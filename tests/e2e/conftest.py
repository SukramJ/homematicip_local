"""Fixtures for the three-way godevccu parity e2e suite.

The backend stack (godevccu + Mosquitto + daemon) is brought up once per
session and shared by all three plane tests; each plane test gets its own
function-scoped Home Assistant instance (via the ``hass`` fixture) so the
three registries never collide on the shared godevccu serial.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
import tempfile

import pytest
import pytest_socket

from .stack import BackendStack, backend_stack, binaries_available


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip the e2e suite unless it is explicitly selected with ``-m e2e``.

    The suite manages real subprocesses and must never run as part of the
    default ``pytest tests`` (xdist) invocation.
    """
    if "e2e" in (config.getoption("markexpr") or ""):
        return
    skip = pytest.mark.skip(reason="three-way parity e2e suite: run explicitly with -m e2e -n0")
    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip)


@pytest.fixture(autouse=True)
def verify_cleanup() -> Iterator[None]:
    """Replace the HA plugin's strict cleanup verifier for the e2e suite.

    The live backends keep resources past a black-box unload that the strict
    verifier turns into failures: aiohomematic's per-interface executor thread
    can outlive ``central.stop()`` (teardown double-stop race), and the loom
    WebSocket listener parks tasks. The plugin exposes fixtures to tolerate
    lingering tasks/timers but none for threads, so the verifier is replaced
    wholesale. The plane tests assert parity, not process hygiene, and each
    runs in its own Home Assistant instance.
    """
    return


@pytest.fixture
def expected_lingering_tasks() -> bool:
    """Tolerate background tasks: the live loom WebSocket listener and the
    aiohomematic client keep tasks running that a black-box unload cannot join.
    """
    return True


@pytest.fixture
def expected_lingering_timers() -> bool:
    """Tolerate background timers from the live backend clients."""
    return True


@pytest.fixture(autouse=True)
def _e2e_enable_sockets() -> None:
    """Re-enable real sockets for every e2e test.

    The HA test plugin disables sockets in ``pytest_runtest_setup`` for each
    test; the e2e suite talks to real loopback servers, so we lift the block.
    """
    pytest_socket.enable_socket()
    pytest_socket.socket_allow_hosts(["127.0.0.1", "::1"], allow_unix_socket=True)


@pytest.fixture(scope="session")
def backend() -> Iterator[BackendStack]:
    """Bring up the shared godevccu + Mosquitto + daemon stack once."""
    ok, reason = binaries_available()
    if not ok:
        pytest.skip(f"e2e backend binaries unavailable: {reason}")
    # The session fixture is created during the first test's setup, after the
    # HA plugin has disabled sockets — re-enable before any network I/O.
    pytest_socket.enable_socket()
    pytest_socket.socket_allow_hosts(["127.0.0.1", "::1"], allow_unix_socket=True)
    with tempfile.TemporaryDirectory(prefix="hmip-e2e-") as td, backend_stack(Path(td)) as stack:
        yield stack


@pytest.fixture(scope="session")
def parity_results() -> dict[str, object]:
    """Collect each plane's scraped snapshot for the final comparison."""
    return {}


@pytest.fixture(scope="session")
def action_results() -> dict[str, object]:
    """Collect each plane's action-probe trace for the final comparison."""
    return {}
