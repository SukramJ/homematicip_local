# Three-way godevccu parity e2e test

`test_three_way_parity.py` drives **one** godevccu backend through **three**
north-bound surfaces and compares the Home Assistant output of each:

| Plane  | Path to godevccu                                              |
| ------ | ------------------------------------------------------------ |
| `ccu`  | `homematicip_local` (aiohomematic) → XML-RPC/JSON-RPC → godevccu |
| `loom` | `homematicip_local` (openccu-loom-client) → REST/WS → daemon → godevccu |
| `mqtt` | daemon MQTT discovery → Mosquitto → HA `mqtt` integration    |

Each plane runs in its own Home Assistant instance (the three share the godevccu
serial, so a single registry would collide). The shared backend stack
(godevccu + Mosquitto + daemon) is started once per session.

## Running

It is **opt-in** and skipped unless the external binaries are present:

```bash
venv/bin/pytest tests/e2e -m e2e -p no:xdist -s
```

`-p no:xdist` is required: the suite manages real processes and ports and must
run serially, and its four tests share session state in definition order
(`ccu` → `loom` → `mqtt` → report).

## Prerequisites

| Binary         | Default location                              | Override env            |
| -------------- | --------------------------------------------- | ----------------------- |
| `godevccu-e2e` | `~/Documents/GitHub/openccu-loom/bin/`        | `GODEVCCU_E2E_BINARY`   |
| `openccu-loom` | `~/Documents/GitHub/openccu-loom/bin/`        | `OPENCCU_LOOM_E2E_BINARY` |
| `mosquitto`    | `$PATH`                                        | `MOSQUITTO_BINARY`      |

Build the Go binaries with `make build` (godevccu) and `make build` /
`go build ./cmd/...` (openccu-loom). `godevccu-e2e` must be built against a
godevccu ≥ 0.1.4 that returns CCU-shaped room/function payloads
(`channelIds: []`, not `null`).

Each plane clears the integration's on-disk cache
(`<config>/homematicip_local`) before setup, so a stale device/paramset cache
from an earlier run cannot pin a plane to a partial device set.

## Status

- `test_parity_report` — always emits the structured diff (per-plane counts and
  every missing/extra/name/attr difference).
- `test_loom_backend_entity_set_parity` — **enforced**: the two
  `homematicip_local` backends (aiohomematic and openccu-loom-client), fed by
  the same godevccu, materialize the same set of entities (one documented
  hub-system-update residual aside).
- `test_full_entity_parity` — `xfail`: tracks the remaining **naming/scheme**
  residuals (not entity-set drift). The loom-client emits a few calculated-DP
  names as raw parameter names and differs on channel/virtual-receiver markers;
  the mqtt discovery layer uses its own naming and unique-id scheme for
  schedules, events and sysvars/programs and labels firmware updates "Firmware"
  vs "Update". These live in the loom-client / daemon naming layers.
