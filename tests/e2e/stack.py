"""Backend-stack orchestration for the three-way parity e2e test.

Brings up, on loopback ephemeral ports, the shared backend consumed by
all three parity planes:

* ``godevccu-e2e`` — a virtual CCU (CCU personality) seeded with a fixed
  HmIP device set, exposing XML-RPC + JSON-RPC and a small control API.
* ``mosquitto`` — a real MQTT broker the daemon publishes discovery to.
* ``openccu-loom`` — the daemon, wired to the godevccu above and the
  Mosquitto above, serving REST/WebSocket for the loom-client backend.

Everything is plain ``subprocess`` + stdlib so the module has no import
dependency on Home Assistant and can be smoke-tested on its own.
"""

from __future__ import annotations

from collections.abc import Iterator
import contextlib
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import time
from typing import IO
import urllib.error
import urllib.request

# Default binary locations. Each is overridable via the matching env var
# so CI or a contributor with a non-standard checkout can point at their
# own builds without editing the test.
_GITHUB = Path.home() / "Documents" / "GitHub"
GODEVCCU_E2E_BIN = os.environ.get("GODEVCCU_E2E_BINARY", str(_GITHUB / "openccu-loom" / "bin" / "godevccu-e2e"))
OPENCCU_LOOM_BIN = os.environ.get("OPENCCU_LOOM_E2E_BINARY", str(_GITHUB / "openccu-loom" / "bin" / "openccu-loom"))
MOSQUITTO_BIN = os.environ.get("MOSQUITTO_BINARY", shutil.which("mosquitto") or "mosquitto")

# Static daemon credentials for the e2e run (loopback only, never shipped).
DAEMON_TOKEN = "e2e-admin-token"
DAEMON_USER = "admin"
DAEMON_PASS = "e2e-admin-pw"
CENTRAL_NAME = "ccu-e2e"
MQTT_TOPIC_BASE = "openccu-loom"

# godevccu's CCU personality uses these credentials. The password must be
# non-empty and pattern-valid: aiohomematic's offline config check rejects an
# empty/invalid password before it ever dials the simulator.
CCU_USERNAME = "Admin"
CCU_PASSWORD = "test"

# Which godevccu device types to expose. The default empty string keeps
# godevccu-e2e's fixed 4-device fast set (deterministic, green, CI-friendly).
# Set GODEVCCU_E2E_DEVICES=all for the comprehensive ~399-type parity report,
# or a comma-separated list to restrict to specific types.
CCU_DEVICES = os.environ.get("GODEVCCU_E2E_DEVICES", "")


def binaries_available() -> tuple[bool, str]:
    """Return (ok, reason) describing whether the stack can be started."""
    missing: list[str] = []
    for label, path in (
        ("godevccu-e2e", GODEVCCU_E2E_BIN),
        ("openccu-loom", OPENCCU_LOOM_BIN),
    ):
        if not Path(path).is_file() or not os.access(path, os.X_OK):
            missing.append(f"{label} ({path})")
    if shutil.which(MOSQUITTO_BIN) is None and not Path(MOSQUITTO_BIN).is_file():
        missing.append(f"mosquitto ({MOSQUITTO_BIN})")
    if missing:
        return False, "missing or non-executable: " + ", ".join(missing)
    return True, ""


def _pick_free_port() -> int:
    """Return a currently-free TCP port on loopback."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_port(port: int, *, host: str = "127.0.0.1", timeout: float = 15.0) -> None:
    """Block until a TCP connect to host:port succeeds or timeout elapses."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        with contextlib.suppress(OSError), socket.create_connection((host, port), timeout=0.5):
            return
        time.sleep(0.05)
    raise TimeoutError(f"port {host}:{port} did not open within {timeout}s")


def _wait_for_http_ok(url: str, *, timeout: float = 60.0) -> None:
    """Block until an HTTP GET of url returns 2xx or timeout elapses."""
    deadline = time.monotonic() + timeout
    last_err: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2.0) as resp:  # noqa: S310 - loopback only
                if 200 <= resp.status < 300:
                    return
        except (urllib.error.URLError, OSError, TimeoutError) as err:
            last_err = err
        time.sleep(0.1)
    raise TimeoutError(f"{url} did not return 2xx within {timeout}s (last error: {last_err})")


@dataclass(slots=True)
class _Managed:
    """A spawned subprocess plus the log file it streams into."""

    name: str
    proc: subprocess.Popen[bytes]
    log: IO[bytes]

    def terminate(self) -> None:
        """Stop the process, escalating to SIGKILL after a grace period."""
        if self.proc.poll() is None:
            self.proc.send_signal(signal.SIGINT)
            try:
                self.proc.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                with contextlib.suppress(subprocess.TimeoutExpired):
                    self.proc.wait(timeout=5.0)
        with contextlib.suppress(Exception):
            self.log.close()


@dataclass(slots=True)
class BackendStack:
    """Resolved coordinates of a running godevccu + daemon + broker stack."""

    workdir: Path
    ccu_host: str
    ccu_xml_rpc_port: int
    ccu_json_rpc_port: int
    ccu_control_port: int
    mqtt_port: int
    daemon_rest_port: int
    _managed: list[_Managed] = field(default_factory=list)

    @property
    def daemon_url(self) -> str:
        """Return the daemon REST base URL."""
        return f"http://127.0.0.1:{self.daemon_rest_port}"

    def set_ccu_value(self, *, address: str, value_key: str, value: object) -> None:
        """Drive a CCU-side state change via the godevccu control API."""
        body = json.dumps({"address": address, "value_key": value_key, "value": value}).encode()
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.ccu_control_port}/set_value",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5.0):  # noqa: S310 - loopback only
            pass

    def stop(self) -> None:
        """Stop every managed process in reverse start order."""
        for managed in reversed(self._managed):
            managed.terminate()
        self._managed.clear()


def _spawn(name: str, args: list[str], *, workdir: Path, cwd: str | None = None) -> _Managed:
    """Spawn a subprocess, streaming combined output to workdir/<name>.log."""
    log_path = workdir / f"{name}.log"
    log = log_path.open("wb")
    proc = subprocess.Popen(
        args,
        stdout=subprocess.PIPE if name == "godevccu" else log,
        stderr=log if name == "godevccu" else subprocess.STDOUT,
        cwd=cwd,
    )
    return _Managed(name=name, proc=proc, log=log)


def _start_godevccu(stack: BackendStack) -> None:
    """Start godevccu-e2e and resolve its advertised ports."""
    managed = _spawn(
        "godevccu",
        [GODEVCCU_E2E_BIN, "-username", CCU_USERNAME, "-password", CCU_PASSWORD, "-devices", CCU_DEVICES],
        workdir=stack.workdir,
    )
    stack._managed.append(managed)
    assert managed.proc.stdout is not None
    # The first stdout line is a single JSON object with the resolved ports.
    raw = managed.proc.stdout.readline()
    if not raw:
        raise RuntimeError("godevccu-e2e exited before advertising ports")
    ports = json.loads(raw.decode())
    stack.ccu_xml_rpc_port = int(ports["xml_rpc_port"])
    stack.ccu_json_rpc_port = int(ports["json_rpc_port"])
    stack.ccu_control_port = int(ports["control_port"])
    # Drain the rest of stdout into the log so the pipe never blocks.
    threading_drain(managed)
    _wait_for_http_ok(f"http://127.0.0.1:{stack.ccu_control_port}/healthz", timeout=15.0)


def threading_drain(managed: _Managed) -> None:
    """Pump remaining godevccu stdout into its log file in a daemon thread."""
    import threading

    def _pump() -> None:
        assert managed.proc.stdout is not None
        with contextlib.suppress(Exception):
            for chunk in iter(lambda: managed.proc.stdout.read(4096), b""):  # type: ignore[union-attr]
                managed.log.write(chunk)

    threading.Thread(target=_pump, daemon=True).start()


def _start_mosquitto(stack: BackendStack) -> None:
    """Start a Mosquitto broker on a free loopback port (anonymous allowed)."""
    port = _pick_free_port()
    conf = stack.workdir / "mosquitto.conf"
    conf.write_text(
        f"listener {port} 127.0.0.1\nallow_anonymous true\npersistence false\n",
        encoding="utf-8",
    )
    managed = _spawn("mosquitto", [MOSQUITTO_BIN, "-c", str(conf)], workdir=stack.workdir)
    stack._managed.append(managed)
    stack.mqtt_port = port
    _wait_for_port(port, timeout=15.0)


def _daemon_config_yaml(stack: BackendStack, data_dir: Path) -> str:
    """Return a complete openccu-loom daemon config for the e2e stack.

    Mirrors tests/e2e/harness/config.go from the openccu-loom repo:
    bearer-token auth, the single central pointed at godevccu, MQTT raw +
    discovery enabled against the local broker.
    """
    callback_port = _pick_free_port()
    bin_port = _pick_free_port()
    ui_port = _pick_free_port()
    return (
        "locale: en\n"
        f'data_dir: "{data_dir}"\n'
        "logging:\n  level: info\n  format: json\n"
        "callback:\n"
        "  host: 127.0.0.1\n"
        f"  port: {callback_port}\n"
        f"  bin_port: {bin_port}\n"
        "north:\n"
        "  rest:\n"
        "    enabled: true\n"
        f'    listen: ":{stack.daemon_rest_port}"\n'
        "    csrf_enabled: false\n"
        "    auth:\n"
        "      basic_enabled: false\n"
        "      bearer_enabled: true\n"
        "      session_enabled: false\n"
        f'      users:\n        {DAEMON_USER}: "{DAEMON_PASS}"\n'
        f"      tokens:\n        {DAEMON_TOKEN}: admin\n"
        "      oidc:\n        enabled: false\n"
        f'  ui:\n    enabled: true\n    listen: ":{ui_port}"\n'
        "  mqtt:\n"
        "    enabled: true\n"
        f'    broker_url: "tcp://127.0.0.1:{stack.mqtt_port}"\n'
        f"    topic_base: {MQTT_TOPIC_BASE}\n"
        "    raw_enabled: true\n"
        "    discovery_enabled: true\n"
        "centrals:\n"
        f"  - name: {CENTRAL_NAME}\n"
        f"    host: {stack.ccu_host}\n"
        f"    port: {stack.ccu_xml_rpc_port}\n"
        f"    json_rpc_port: {stack.ccu_json_rpc_port}\n"
        f"    username: {CCU_USERNAME}\n"
        f'    password: "{CCU_PASSWORD}"\n'
        "    interfaces:\n      - HmIP-RF\n"
    )


def _start_daemon(stack: BackendStack) -> None:
    """Start the openccu-loom daemon and wait until it reports healthy."""
    stack.daemon_rest_port = _pick_free_port()
    data_dir = stack.workdir / "daemon-data"
    data_dir.mkdir(exist_ok=True)
    cfg_path = stack.workdir / "daemon-config.yaml"
    cfg_path.write_text(_daemon_config_yaml(stack, data_dir), encoding="utf-8")
    managed = _spawn(
        "daemon",
        [OPENCCU_LOOM_BIN, "run", "--config", str(cfg_path)],
        workdir=stack.workdir,
    )
    stack._managed.append(managed)
    # Seeding the full ~399-device set over JSON-RPC takes a while.
    _wait_for_http_ok(f"{stack.daemon_url}/api/v1/health", timeout=300.0)


@contextlib.contextmanager
def backend_stack(workdir: Path) -> Iterator[BackendStack]:
    """Context manager yielding a fully-wired, healthy BackendStack.

    Starts godevccu, Mosquitto and the daemon (in that order) and tears
    them all down on exit, even if startup of a later stage fails.
    """
    stack = BackendStack(
        workdir=workdir,
        ccu_host="127.0.0.1",
        ccu_xml_rpc_port=0,
        ccu_json_rpc_port=0,
        ccu_control_port=0,
        mqtt_port=0,
        daemon_rest_port=0,
    )
    try:
        _start_godevccu(stack)
        _start_mosquitto(stack)
        _start_daemon(stack)
        yield stack
    finally:
        stack.stop()
