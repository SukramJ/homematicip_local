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
venv/bin/pytest tests/e2e -m e2e -n0 -s
```

`-n0` is required: the suite manages real processes and ports and must run
serially, and its tests share session state in definition order (`ccu` →
`loom` → `mqtt` → parity). (Don't use `-p no:xdist` — the repo's default
`addopts` passes `-n auto --dist loadscope`, which then errors as unrecognized
once the xdist plugin is disabled; `-n0` keeps xdist loaded but runs in-process.)

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

## Device set

By default the suite uses `godevccu-e2e`'s fixed **4-device** set (one per HA
domain shape) — fast (~1 min), deterministic, and the basis for the enforced
parity assertions.

Set `GODEVCCU_E2E_DEVICES` to widen coverage:

```bash
# comprehensive: every embedded godevccu type (~399), ~2 min
GODEVCCU_E2E_DEVICES=all venv/bin/pytest tests/e2e -m e2e -n0 -s
# a specific subset
GODEVCCU_E2E_DEVICES=HmIP-BDT,HmIP-SWDO venv/bin/pytest tests/e2e -m e2e -n0 -s
```

The `all` run is a **diagnostic report**, not a green gate: at full scale the
backends diverge substantially (the aiohomematic plane exposes ~750
`PRESS_SHORT`/`PRESS_LONG` virtual-key button entities the loom-client/mqtt
planes do not; calc-DP/virtual-key name doubling; cover/light feature-flag and
unit differences). Read `test_parity_report`'s output to triage; the strict
`test_entity_set_parity` is expected to fail there until those gaps are closed.

Each plane clears the integration's on-disk cache
(`<config>/homematicip_local`) before setup, so a stale device/paramset cache
from an earlier run cannot pin a plane to a partial device set.

## Status

- `test_parity_report` — always emits the structured diff (per-plane counts and
  every missing/extra/name/attr difference).
- `test_entity_set_parity` — **enforced**: all three planes — aiohomematic,
  openccu-loom-client and the daemon's mqtt discovery, fed by the same godevccu
  — materialize the same set of entities. A small documented by-design allowlist
  applies: the hub system-update (only the daemon-backed planes create it) and
  the admin/maintenance entities the mqtt discovery deliberately omits (program
  *buttons*, the install-mode button + sensor, the backup button).
- `test_full_entity_parity` — `xfail`: tracks the remaining **name/attribute**
  residuals (not entity-set drift):
  - **loom** — only the multi-channel ` chN` marker remains. It needs
    paramset-description-level presence (a parameter defined on several channels
    even when active on one), which the daemon's active-data-point model does not
    expose. The schedule-switch target-channel names are fixed (daemon api 1.7.0
    ships `available_target_channels`).
  - **mqtt** — the discovery layer uses HA-idiomatic naming (sysvar display
    names, no channel-type / `P ` / `SV ` prefixes, `Firmware` vs `Update`) and
    sets `unit`/`state_class` on sysvars.

The comparison normalizes away per-run instance/central/serial tokens, the
`calculated`/`combined` markers, the mqtt domain suffix and the differing
event / schedule / week-profile unique-id schemes, and compares the stable
registry `original_name` (not the timing-dependent live `friendly_name`); card
attributes are compared only when both planes have reported a state.

Requires openccu-loom-client ≥ 2026.6.13 (calculated-DP names match the
direct-CCU twin).
