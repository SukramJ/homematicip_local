"""Three-way godevccu parity end-to-end test suite.

This package orchestrates a single godevccu backend behind three
north-bound surfaces and asserts the Home Assistant entity/device output
is identical across them:

1. homematicip_local with the aiohomematic backend, talking XML-RPC /
   JSON-RPC directly to godevccu (the reference).
2. homematicip_local with the openccu-loom-client backend, talking
   REST / WebSocket to a local openccu-loom daemon that itself talks to
   the same godevccu.
3. The openccu-loom daemon's MQTT discovery, consumed by Home
   Assistant's mqtt integration via a real Mosquitto broker.

The suite is opt-in (``pytest -m e2e``) and skips unless the external Go
binaries and Mosquitto are available.
"""

from __future__ import annotations
