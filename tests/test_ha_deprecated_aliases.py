"""
Guard against runtime imports of Home Assistant's undefined sentinel names.

From HA 2026.12 on, `homeassistant.helpers.typing` keeps `UNDEFINED` and
`UndefinedType` only as `DeprecatedAlias` entries of the sentinel `Undefined`,
served through the module's `__getattr__` (`check_if_deprecated_constant`).
Every runtime `from homeassistant.helpers.typing import UNDEFINED` therefore
logs "The deprecated alias UNDEFINED was used from homematicip_local", and the
aliases go away in HA 2027.12. `Undefined` itself does not exist on the minimum
HA version 2026.11 yet, so a runtime import of it would fail there with
`ImportError`. The integration names `Undefined` in annotations only, under
`if TYPE_CHECKING:`; `Undefined` leaves the guarded set once the minimum HA
version is 2026.12 or later.

The pinned HA in the test suite does not deprecate the aliases, so the warning
cannot be observed at runtime here; the guard reads the source instead.
"""

from __future__ import annotations

import ast
from pathlib import Path

_PACKAGE = Path(__file__).resolve().parents[1] / "custom_components" / "homematicip_local"
_TYPING_MODULE = "homeassistant.helpers.typing"
_TYPING_ONLY = frozenset({"UNDEFINED", "UndefinedType", "Undefined"})


def _is_type_checking_block(node: ast.AST) -> bool:
    """Return whether the node is an `if TYPE_CHECKING:` block."""
    return (
        isinstance(node, ast.If)
        and isinstance(node.test, ast.Name | ast.Attribute)
        and (node.test.id if isinstance(node.test, ast.Name) else node.test.attr) == "TYPE_CHECKING"
    )


def _runtime_violations(*, path: Path) -> list[str]:
    """Return the typing-only names a module imports outside `if TYPE_CHECKING:`."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    violations: list[str] = []

    def visit(node: ast.AST) -> None:
        if _is_type_checking_block(node):
            # The body is typing-only; an `else` branch would run.
            for child in getattr(node, "orelse", []):
                visit(child)
            return
        if isinstance(node, ast.ImportFrom) and node.module == _TYPING_MODULE:
            violations.extend(
                f"{path.relative_to(_PACKAGE)}:{node.lineno} imports {alias.name}"
                for alias in node.names
                if alias.name in _TYPING_ONLY
            )
        for child in ast.iter_child_nodes(node):
            visit(child)

    visit(tree)
    return violations


def test_no_runtime_access_to_deprecated_undefined_aliases() -> None:
    """No integration module imports UNDEFINED, UndefinedType or Undefined at runtime."""
    violations = [
        violation
        for path in sorted(_PACKAGE.rglob("*.py"))
        if "frontend" not in path.parts
        for violation in _runtime_violations(path=path)
    ]
    assert not violations, "typing-only HA names imported at runtime:\n" + "\n".join(violations)
