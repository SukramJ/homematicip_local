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

The suite asserts parity on three levels:

1. **Entity set** (`test_entity_set_parity`, enforced) — same entities on
   every plane.
2. **Behavior** (`test_action_parity` + `test_config_surface_parity`,
   enforced) — identical HA service calls (switch toggle, cover position,
   climate target temperature) and a CCU-side push converge to identical
   states on every plane; both `homematicip_local` backends serve the same
   VALUES paramset description for the probed channel. Every probe restores
   the state it found, so the shared backend is unchanged for the next plane.
3. **Names/attributes** (`test_full_entity_parity`, xfail) — tracks the
   residual naming/attribute drift documented below.

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

In CI the suite runs via `.github/workflows/e2e-parity.yaml`: the default set
as a gate on dependency-bump PRs (manifest.json / requirements_test.txt) and
nightly, plus a nightly full-set (`GODEVCCU_E2E_DEVICES=all`) report job whose
log artifact carries the ratchet summary.

## Prerequisites

| Binary         | Default location                              | Override env            |
| -------------- | --------------------------------------------- | ----------------------- |
| `godevccu-e2e` | `~/Documents/GitHub/openccu-loom/bin/`        | `GODEVCCU_E2E_BINARY`   |
| `openccu-loom` | `~/Documents/GitHub/openccu-loom/bin/`        | `OPENCCU_LOOM_E2E_BINARY` |
| `mosquitto`    | `$PATH`                                        | `MOSQUITTO_BINARY`      |

Build the Go binaries with `make build-all` in the openccu-loom repo. The
backend stack must match the pinned Python clients:

- The daemon must serve the wire surface the pinned `openccu-loom-client`
  expects (e.g. client 2026.7.16 reads `/info.addon_build`) and must stamp
  **channel-level** custom-DP unique_ids (aiohomematic's key shape; daemon >
  0.48.8).
- `godevccu` must answer aiohomematic's `get_alarm_messages.fn` with a
  dedicated (empty) alarm list instead of misrouting it to the sysvar
  handlers (godevccu > 0.1.8), and reports CCU-semantics serials (the
  trailing 10 characters — the suite's `SERIAL` constant matches the
  *reported* serial).
- `godevccu-e2e` (the driver in the openccu-loom repo) must mirror
  virtual-receiver writes onto the `…_TRANSMITTER` state channel (real HmIP
  actuator firmware semantics) — without it the aiohomematic plane's custom
  data points, which read state from the transmitter channel, never see a
  service call take effect and the action probes time out.

`MOSQUITTO_BINARY` may point at a wrapper script (e.g. one that runs the
broker from the `eclipse-mosquitto` Docker image) as long as it accepts
`-c <conf>`; note a snap-installed Docker daemon cannot mount configs from
`/tmp`, so redirect `TMPDIR` to a `$HOME` path for the pytest run in that
setup.

## Device set

By default the suite uses `godevccu-e2e`'s fixed **4-device** set (one per HA
domain shape: HmIP-BROLL, HmIP-BSM, HmIP-BWTH, HmIP-SWSD) — fast (~1 min),
deterministic, and fully enforced.

Set `GODEVCCU_E2E_DEVICES` to widen coverage:

```bash
# comprehensive: every embedded godevccu type (~399), ~2 min
GODEVCCU_E2E_DEVICES=all venv/bin/pytest tests/e2e -m e2e -n0 -s
# a specific subset
GODEVCCU_E2E_DEVICES=HmIP-BDT,HmIP-SWDO venv/bin/pytest tests/e2e -m e2e -n0 -s
```

## The ratchet (widened runs)

In a widened run `test_entity_set_parity` enforces only entities backed by a
model in `enforced_models.py` (plus all hub/central entities); the long tail
of not-yet-promoted models is *reported*, not asserted. The `PARITY REPORT`
printed by `test_parity_report` carries the ratchet summary:

- `promotable_models` — clean across all three planes but not yet enforced:
  add them to `ENFORCED_MODELS` and commit; from then on they cannot silently
  regress.
- `regressed_enforced_models` — enforced models that drifted; these fail the
  parity test.

The ratchet only widens. The end state is every godevccu model enforced, at
which point `GODEVCCU_E2E_DEVICES=all` is a green gate. See
`enforced_models.py` for the workflow.

**Current full-set status:** the aiohomematic plane does not finish its
initial load at full scale — the ~399-model paramset-description fetch
against godevccu exceeds the 900 s settle budget (the settle floor now
surfaces this as a `TimeoutError` instead of silently comparing a partial
scrape, which is what a pre-floor run did: 23 hub entities vs ~5 600 device
entities on the daemon planes). Until that upstream load path is fixed, the
full-set CI job is `continue-on-error` and the 4-device gate is the enforced
one.

Each plane clears the integration's on-disk cache
(`<config>/homematicip_local`) before setup, so a stale device/paramset cache
from an earlier run cannot pin a plane to a partial device set.

## Status

- `test_parity_report` — always emits the structured diff (per-plane counts,
  every missing/extra/name/attr difference, ratchet summary).
- `test_entity_set_parity` — **enforced** (ratchet-scoped in widened runs). A
  small documented by-design allowlist applies: the hub system-update (only
  the daemon-backed planes create it) and the admin/maintenance entities the
  mqtt discovery deliberately omits (program *buttons*, the install-mode
  button + sensor, the backup button).
- `test_action_parity` / `test_config_surface_parity` — **enforced**: the
  behavioral probes above.
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

The e2e conftest replaces the HA test plugin's strict cleanup verifier: the
live aiohomematic client can keep its per-interface executor thread past a
black-box unload, and the plugin exposes no fixture to tolerate threads. The
plane helper likewise tolerates `BaseHomematicException` from the unload
itself (aiohomematic 2026.7.11 can raise on a double stop request) — the
suite asserts parity, not teardown hygiene.
