"""
Contract tests for the dual-backend (aiohomematic / openccu-loom) central surface.

STABILITY GUARANTEE
-------------------
The integration drives both backends through one facade shape: aiohomematic's
``CentralUnit`` on the direct-CCU backend and openccu-loom-client's duck-typed
``LoomCentralAdapter`` on the loom backend. aiohomematic's Protocol metaclass
blocks subclassing, so that bridge is *not* statically type-checked — drift
between the two surfaces would otherwise only break at runtime.

These tests close that hole:

1. Every ``central.<member>`` the integration accesses exists on BOTH backend
   central classes.
2. Every ``central.<facade>.<member>`` the integration accesses exists on both
   resolved facade classes, and shared methods are call-compatible (the loom
   side accepts every parameter the aiohomematic side declares and requires
   nothing extra).
3. Every exported dispatch tuple in ``backend_types.py`` carries a loom twin
   for each aiohomematic class (and is never empty while openccu-loom-client
   is installed).
4. No integration module ``isinstance``-dispatches on a concrete aiohomematic
   data-point class outside ``backend_types.py`` — a loom data point is never
   an instance of an aiohomematic class, so such a check silently drops the
   loom backend.

The used-surface inventory is rebuilt from the integration sources via AST on
every run, so new call sites are covered automatically. Deliberate, guarded
divergences (e.g. ``getattr(central, "x", None)`` probes) never appear in the
inventory because they are not plain attribute accesses.
"""

from __future__ import annotations

import ast
import dataclasses
import enum
import importlib
import inspect
from pathlib import Path
import sys
import textwrap
import typing
from typing import Any

from openccu_loom_client.compat.aiohomematic.central.adapter import LoomCentralAdapter

from aiohomematic.central import CentralUnit

INTEGRATION_ROOT = Path(__file__).parent.parent.parent / "custom_components" / "homematicip_local"

# ---------------------------------------------------------------------------
# Documented exemptions. Every entry must state a reason; an empty dict is the
# healthy baseline — additions mean a real, accepted parity gap.
# ---------------------------------------------------------------------------

# central members the loom adapter deliberately does not provide. Accesses to
# these must be guarded at the call site (e.g. via getattr with default).
LOOM_EXEMPT_CENTRAL_MEMBERS: dict[str, str] = {}

# facade members missing on one side, keyed by "<facade>.<member>".
EXEMPT_FACADE_MEMBERS: dict[str, str] = {}

# Known call-shape gaps, keyed by "<facade>.<member>". Every entry is a REAL,
# reachable runtime break on the loom backend, tracked for a fix in
# openccu-loom-client's compat adapter; remove the entry once the adapter
# accepts the aiohomematic call shape.
EXEMPT_FACADE_CALLS: dict[str, str] = {
    "device_coordinator.delete_device": (
        "loom signature is (*, address) vs aiohomematic's (*, interface_id, device_address); "
        "removing a device from HA raises TypeError on a loom entry (__init__.py)."
    ),
    "device_coordinator.create_central_links": (
        "loom requires address; the central-wide no-arg service call "
        "(services.py create_central_links) raises TypeError on a loom entry."
    ),
    "device_coordinator.remove_central_links": (
        "loom requires address; the central-wide no-arg service call "
        "(services.py remove_central_links) raises TypeError on a loom entry."
    ),
    "configuration.get_link_paramset_description": (
        "loom additionally requires peer; the link config panel call "
        "(websocket_api.py) raises TypeError on a loom entry."
    ),
}

# facades whose class cannot be resolved generically (annotation is Any or an
# unresolvable forward ref); mapped to an explicit (aiohomematic, loom) class
# pair so their members are still verified instead of silently skipped.
_FACADE_CLASS_OVERRIDES: dict[str, tuple[type, type] | None] = {}

# isinstance dispatch sites on concrete aiohomematic model classes outside
# backend_types.py, keyed by "<file>:<name>". Empty baseline: every dispatch
# goes through backend_types pairs or runtime-checkable Protocols.
EXEMPT_ISINSTANCE_SITES: dict[str, str] = {
    "device_trigger.py:ClickEvent": (
        "event objects are real aiohomematic instances on both backends — the loom "
        "adapter republishes aiohomematic events on a real aiohomematic EventBus, "
        "so this isinstance check holds for loom data too."
    ),
}


def _override_config_pair() -> tuple[type, type]:
    """Return the (aiohomematic, loom) classes behind ``central.config``.

    Both ``config`` properties are annotated too loosely for generic
    resolution (the loom side returns ``Any``), so the pair is pinned here.
    """
    from openccu_loom_client.config import LoomConfig

    from aiohomematic.central import CentralConfig

    return (CentralConfig, LoomConfig)


_FACADE_CLASS_OVERRIDES["config"] = _override_config_pair()


# ---------------------------------------------------------------------------
# AST inventory of the surface the integration actually uses
# ---------------------------------------------------------------------------


def _integration_sources() -> list[Path]:
    """Return all integration source files."""
    return sorted(INTEGRATION_ROOT.rglob("*.py"))


def _is_central_base(node: ast.expr) -> bool:
    """Return whether an expression is a reference to a central unit."""
    if isinstance(node, ast.Name):
        return node.id in ("central", "_central")
    if isinstance(node, ast.Attribute):
        return node.attr in ("central", "_central")
    return False


def _used_central_surface() -> tuple[set[str], dict[str, set[str]]]:
    """Return (first-level members, facade -> second-level members) in use."""
    first: set[str] = set()
    second: dict[str, set[str]] = {}
    for source in _integration_sources():
        tree = ast.parse(source.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Attribute):
                continue
            if _is_central_base(node.value):
                first.add(node.attr)
            inner = node.value
            if isinstance(inner, ast.Attribute) and _is_central_base(inner.value):
                second.setdefault(inner.attr, set()).add(node.attr)
    return first, second


@dataclasses.dataclass(frozen=True, slots=True)
class _CallSite:
    """One ``central.<facade>.<member>(...)`` call as written in the sources."""

    location: str
    keywords: frozenset[str]
    has_positional: bool
    has_star_kwargs: bool


def _used_facade_calls() -> dict[tuple[str, str], list[_CallSite]]:
    """Return every ``central.<facade>.<member>(...)`` call with its arguments."""
    calls: dict[tuple[str, str], list[_CallSite]] = {}
    for source in _integration_sources():
        tree = ast.parse(source.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            inner = node.func.value
            if not (isinstance(inner, ast.Attribute) and _is_central_base(inner.value)):
                continue
            calls.setdefault((inner.attr, node.func.attr), []).append(
                _CallSite(
                    location=f"{source.name}:{node.lineno}",
                    keywords=frozenset(kw.arg for kw in node.keywords if kw.arg is not None),
                    has_positional=bool(node.args),
                    has_star_kwargs=any(kw.arg is None for kw in node.keywords),
                )
            )
    return calls


# ---------------------------------------------------------------------------
# Class-level member and facade-class resolution (no instantiation)
# ---------------------------------------------------------------------------


def _init_assignments(cls: type) -> dict[str, ast.expr]:
    """Return ``self.<name> = <expr>`` assignments from the class's __init__ chain."""
    assignments: dict[str, ast.expr] = {}
    for klass in cls.__mro__:
        init = klass.__dict__.get("__init__")
        if init is None or not inspect.isfunction(init):
            continue
        try:
            source = textwrap.dedent(inspect.getsource(init))
        except OSError, TypeError:
            continue
        for node in ast.walk(ast.parse(source)):
            target: ast.expr | None = None
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
            elif isinstance(node, ast.AnnAssign):
                target = node.target
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "self"
                and node.value is not None
                and target.attr not in assignments
            ):
                assignments[target.attr] = node.value
    return assignments


def _member_exists(cls: type, name: str) -> bool:
    """Return whether a class provides a member (descriptor, method, field or instance attr)."""
    if inspect.getattr_static(cls, name, None) is not None:
        return True
    if dataclasses.is_dataclass(cls) and name in {f.name for f in dataclasses.fields(cls)}:
        return True
    # pydantic models expose fields via model_fields; plain annotated class
    # attributes only via __annotations__ (both are invisible to getattr_static).
    if name in getattr(cls, "model_fields", {}):
        return True
    if any(name in klass.__dict__.get("__annotations__", {}) for klass in cls.__mro__):
        return True
    return name in _init_assignments(cls)


def _class_from_call(node: ast.expr, module: Any) -> type | None:
    """Resolve the class (or factory return class) behind ``Something(...)``."""
    if not isinstance(node, ast.Call):
        return None
    func = node.func
    name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", None)
    if name is None:
        return None
    resolved = getattr(module, name, None)
    if inspect.isclass(resolved):
        return resolved
    if callable(resolved):
        try:
            return_hint = typing.get_type_hints(resolved).get("return")
        except Exception:
            return None
        if inspect.isclass(return_hint):
            return return_hint
    return None


def _resolve_attr_class(cls: type, name: str) -> type | None:
    """Resolve the class of ``instance.<name>`` without instantiating ``cls``.

    Handles plain properties (via return annotation), aiohomematic's
    ``DelegatedProperty`` (by following its delegation path through __init__
    assignments) and direct ``self.<name> = Class(...)`` __init__ assignments.
    """
    descriptor = inspect.getattr_static(cls, name, None)
    if isinstance(descriptor, property) and descriptor.fget is not None:
        try:
            return_hint = typing.get_type_hints(descriptor.fget).get("return")
        except Exception:
            return None
        return return_hint if inspect.isclass(return_hint) else None
    parts = getattr(descriptor, "_parts", None)
    if parts:  # aiohomematic DelegatedProperty: follow the delegation path
        current: type | None = cls
        for part in parts:
            if current is None:
                return None
            current = _resolve_attr_class(current, part)
        return current
    # Anything else (absent, or a slot member_descriptor of a __slots__ class)
    # is an instance attribute: resolve it from the __init__ assignments.
    return _resolve_attr_class_via_init(cls, name)


def _resolve_attr_class_via_init(cls: type, name: str) -> type | None:
    """Resolve the class assigned to ``self.<name>`` in ``cls.__init__``."""
    value = _init_assignments(cls).get(name)
    if value is None:
        return None
    for klass in cls.__mro__:
        if name in _init_assignments(klass):
            module = sys.modules[klass.__module__]
            return _class_from_call(value, module)
    return None


def _facade_pair(facade: str) -> tuple[type, type] | str:
    """Return the resolved (aiohomematic, loom) facade classes or a skip reason."""
    if facade in _FACADE_CLASS_OVERRIDES:
        override = _FACADE_CLASS_OVERRIDES[facade]
        return override if override is not None else f"override skip: {facade}"
    aio_cls = _resolve_attr_class(CentralUnit, facade)
    loom_cls = _resolve_attr_class(LoomCentralAdapter, facade)
    if aio_cls is None or loom_cls is None:
        return f"unresolved facade {facade!r}: aio={aio_cls} loom={loom_cls} — add a _FACADE_CLASS_OVERRIDES entry"
    return (aio_cls, loom_cls)


# ---------------------------------------------------------------------------
# 1 + 2: used central surface exists on both backends
# ---------------------------------------------------------------------------


def test_used_central_members_exist_on_both_backends() -> None:
    """Contract: every central member the integration uses exists on both backends."""
    first, _ = _used_central_surface()
    assert first, "AST inventory found no central usage — scan is broken"
    missing_aio = sorted(m for m in first if not _member_exists(CentralUnit, m))
    missing_loom = sorted(
        m for m in first if not _member_exists(LoomCentralAdapter, m) and m not in LOOM_EXEMPT_CENTRAL_MEMBERS
    )
    assert not missing_aio, f"used central members missing on aiohomematic CentralUnit: {missing_aio}"
    assert not missing_loom, (
        f"used central members missing on LoomCentralAdapter: {missing_loom} — "
        "either add them to openccu-loom-client's compat adapter, or guard the call "
        "site and document the gap in LOOM_EXEMPT_CENTRAL_MEMBERS"
    )
    stale = sorted(set(LOOM_EXEMPT_CENTRAL_MEMBERS) - first)
    assert not stale, f"stale LOOM_EXEMPT_CENTRAL_MEMBERS entries (no longer used): {stale}"


def test_used_facade_members_exist_on_both_backends() -> None:
    """Contract: every used facade member exists on both resolved facade classes."""
    _, second = _used_central_surface()
    assert second, "AST inventory found no facade usage — scan is broken"
    problems: list[str] = []
    for facade, members in sorted(second.items()):
        if facade in LOOM_EXEMPT_CENTRAL_MEMBERS:
            continue
        pair = _facade_pair(facade)
        if isinstance(pair, str):
            problems.append(pair)
            continue
        aio_cls, loom_cls = pair
        for member in sorted(members):
            key = f"{facade}.{member}"
            if key in EXEMPT_FACADE_MEMBERS:
                continue
            if not _member_exists(aio_cls, member):
                problems.append(f"{key} missing on aiohomematic {aio_cls.__name__}")
            if not _member_exists(loom_cls, member):
                problems.append(f"{key} missing on loom {loom_cls.__name__}")
    assert not problems, "facade surface drift:\n  " + "\n  ".join(problems)


def _call_problems(*, side: str, method: Any, key: str, sites: list[_CallSite]) -> list[str]:
    """Return incompatibilities between recorded call sites and one side's method."""
    if not inspect.isfunction(method):
        return []
    params = {n: p for n, p in inspect.signature(method).parameters.items() if n != "self"}
    has_var_keyword = any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values())
    accepts_positional = any(
        p.kind
        in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.VAR_POSITIONAL,
        )
        for p in params.values()
    )
    required = {
        n
        for n, p in params.items()
        if p.default is inspect.Parameter.empty
        and p.kind in (inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    }
    problems: list[str] = []
    for site in sites:
        if site.has_star_kwargs:
            continue  # a **kwargs call cannot be checked statically
        rejected = sorted(kw for kw in site.keywords if kw not in params and not has_var_keyword)
        unsatisfied = sorted(required - site.keywords) if not site.has_positional else []
        if rejected:
            problems.append(f"{key} at {site.location}: {side} does not accept {rejected}")
        if unsatisfied:
            problems.append(f"{key} at {site.location}: {side} requires {unsatisfied} the call does not pass")
        if site.has_positional and not accepts_positional:
            problems.append(f"{key} at {site.location}: {side} takes keyword-only arguments")
    return problems


def test_used_facade_calls_are_compatible_with_both_backends() -> None:
    """Contract: every facade call, as written, is accepted by both backends.

    Only arguments actually passed at the call sites are checked, so optional
    parameters existing on one side only never trip the contract. Async-ness is
    deliberately not compared: the integration awaits results only when the
    backend returns an awaitable.
    """
    calls = _used_facade_calls()
    assert calls, "AST inventory found no facade calls — scan is broken"
    problems: list[str] = []
    for (facade, member), sites in sorted(calls.items()):
        key = f"{facade}.{member}"
        if key in EXEMPT_FACADE_CALLS or facade in LOOM_EXEMPT_CENTRAL_MEMBERS:
            continue
        pair = _facade_pair(facade)
        if isinstance(pair, str):
            continue  # reported by the presence test
        aio_cls, loom_cls = pair
        problems += _call_problems(
            side="aiohomematic", method=inspect.getattr_static(aio_cls, member, None), key=key, sites=sites
        )
        problems += _call_problems(
            side="loom", method=inspect.getattr_static(loom_cls, member, None), key=key, sites=sites
        )
    assert not problems, "facade call-shape drift (each entry breaks at runtime on that backend):\n  " + "\n  ".join(
        problems
    )
    stale = sorted(set(EXEMPT_FACADE_CALLS) - {f"{f}.{m}" for f, m in calls})
    assert not stale, f"stale EXEMPT_FACADE_CALLS entries (no longer called): {stale}"


# ---------------------------------------------------------------------------
# 3: backend_types dispatch tuples carry loom twins
# ---------------------------------------------------------------------------


def test_backend_types_tuples_carry_loom_twins() -> None:
    """Contract: every backend_types dispatch tuple pairs each aiohomematic class with a loom twin."""
    backend_types = importlib.import_module("custom_components.homematicip_local.backend_types")
    checked = 0
    problems: list[str] = []
    for name, value in vars(backend_types).items():
        if not name.isupper() or not isinstance(value, tuple):
            continue
        checked += 1
        if not value:
            problems.append(f"{name} is empty although openccu-loom-client is installed")
            continue
        aio_members = [c for c in value if c.__module__.startswith("aiohomematic")]
        loom_members = [c for c in value if c.__module__.startswith("openccu_loom_client")]
        unknown = [c for c in value if c not in aio_members and c not in loom_members]
        if unknown:
            problems.append(f"{name} contains classes from unexpected modules: {unknown}")
        if len(loom_members) < len(aio_members):
            missing = [c.__name__ for c in aio_members]
            problems.append(f"{name}: loom twin missing (aio={missing}, loom={[c.__name__ for c in loom_members]})")
    assert checked, "no dispatch tuples found in backend_types — module layout changed?"
    assert not problems, "backend_types twin drift:\n  " + "\n  ".join(problems)


# ---------------------------------------------------------------------------
# 4: no concrete aiohomematic model class isinstance dispatch outside backend_types
# ---------------------------------------------------------------------------


def _isinstance_class_refs(tree: ast.Module) -> set[str]:
    """Return names referenced as the class argument of isinstance() calls."""
    names: set[str] = set()

    def _collect(node: ast.expr) -> None:
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.Tuple):
            for element in node.elts:
                _collect(element)
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            _collect(node.left)
            _collect(node.right)
        elif isinstance(node, ast.Starred):
            _collect(node.value)

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "isinstance"
            and len(node.args) == 2
        ):
            _collect(node.args[1])
    return names


def _aiohomematic_model_imports(tree: ast.Module) -> dict[str, str]:
    """Return imported-name -> module for imports from aiohomematic.model*."""
    imports: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("aiohomematic.model"):
            for alias in node.names:
                imports[alias.asname or alias.name] = node.module
    return imports


def _is_concrete_model_class(module_name: str, symbol: str) -> bool:
    """Return whether a symbol is a concrete (dispatch-unsafe) model class."""
    obj = getattr(importlib.import_module(module_name), symbol, None)
    if not inspect.isclass(obj):
        return False
    if getattr(obj, "_is_protocol", False):
        return False
    return not issubclass(obj, (enum.Enum, BaseException))


def test_no_bare_aiohomematic_isinstance_dispatch() -> None:
    """Contract: platforms never isinstance-dispatch on concrete aiohomematic model classes.

    A loom data point is never an instance of an aiohomematic class (the
    Protocol metaclass blocks subclassing), so such a check silently excludes
    the loom backend. Dispatch must go through the paired tuples in
    ``backend_types.py`` or runtime-checkable Protocols.
    """
    violations: list[str] = []
    for source in _integration_sources():
        if source.name == "backend_types.py":
            continue
        tree = ast.parse(source.read_text(encoding="utf-8"))
        model_imports = _aiohomematic_model_imports(tree)
        if not model_imports:
            continue
        for name in sorted(_isinstance_class_refs(tree) & set(model_imports)):
            site = f"{source.name}:{name}"
            if site in EXEMPT_ISINSTANCE_SITES:
                continue
            if _is_concrete_model_class(model_imports[name], name):
                violations.append(site)
    assert not violations, (
        f"concrete aiohomematic model classes used in isinstance dispatch: {violations} — "
        "route the check through a backend_types tuple (or document the site in EXEMPT_ISINSTANCE_SITES)"
    )
