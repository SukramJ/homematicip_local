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
godevccu that returns CCU-shaped room/function payloads (`channelIds: []`, not
`null`).

## Status

`test_parity_report` always emits the structured diff. `test_full_entity_parity`
is currently `xfail`: the aiohomematic plane creates generic entities
data-driven from godevccu's `fetch_all_device_data`, which today returns only
datapoints that carry a stored value and in a non-CCU shape — so it
under-creates relative to the description-driven `loom`/`mqtt` planes. Once
godevccu emits the complete, CCU-shaped device-data payload the strict test is
expected to pass.
