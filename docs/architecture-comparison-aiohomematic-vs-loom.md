# Architecture Comparison: `aiohomematic` (direct CCU) vs. OpenCCU-Loom

**Scope:** A deep, cross-verified comparison of the two backend architectures that
power (or are being prepared to power) the Home Assistant integration
*Homematic(IP) Local for OpenCCU* (`homematicip_local`):

1. **`aiohomematic`** — the classic, production backend. A Python library that
   talks **directly** to the Homematic CCU over XML-RPC + JSON-RPC, running
   in-process inside Home Assistant.
2. **OpenCCU-Loom** — a newer split architecture: a standalone **Go daemon**
   (`openccu-loom`) that owns the CCU connection and exposes a REST + WebSocket
   API, consumed by a **thin Python client** (`openccu-loom-client`) whose
   `compat/aiohomematic` layer mimics the aiohomematic API so the integration
   can use either backend.

**Status at time of writing** (2026-06-21, branch `feat/loom-client-2026.6.20`,
integration v2.8.0): the Loom backend is **bundled but not user-selectable** —
`LOOM_BACKEND_SELECTABLE = False` (`custom_components/homematicip_local/const.py:65`).
It is groundwork for a future alternative, not a shipping feature.

> **Method note.** This document was produced by reading the installed package
> sources (`venv/.../aiohomematic`, `.../openccu_loom_client`,
> `.../openccu_loom_types`), the integration code under
> `custom_components/homematicip_local/`, and the daemon repository at
> `../openccu-loom` (README, SPECIFICATION, 42 ADRs, OpenAPI/WS contracts, Go
> sources). Code references are given as `file:line` where available. Version
> strings observed in source occasionally lag the build (e.g. the client's
> `const.py` reports `2026.6.19`; the daemon README header says `0.2.0` while
> CHANGELOG/API report `0.7.1` / API `1.17.0`).

---

## 1. Executive summary

| | `aiohomematic` (direct) | OpenCCU-Loom (daemon + thin client) |
|---|---|---|
| **Shape** | One in-process library, HA ↔ CCU | Standalone Go daemon between HA and CCU |
| **Code size** | ~74,130 LOC Python (200 files) | Client ~13,985 LOC Python + types ~2,479 LOC + **daemon ~231,923 LOC Go** |
| **HA-process footprint** | Heavy (full library) | Thin (~14k LOC adapter) |
| **South-bound (to CCU)** | XML-RPC + JSON-RPC | XML-RPC + **BIN-RPC** + JSON-RPC |
| **North-bound (to HA)** | n/a (is in-process) | REST + WebSocket (JSON, delta push) |
| **Inbound listener in HA?** | **Yes** (local XML-RPC callback server) | **No** (single outgoing WebSocket) |
| **Typical CCU hop** | LAN | **Loopback** when daemon runs on the CCU |
| **Maturity in HA today** | Production (default backend) | Disabled groundwork; daemon-side parity gaps largely closed (daemon API 1.18.0), client consumption pending |
| **Extra surfaces** | HA only | MQTT (HA Discovery), Matter, Web Config-UI |

**The central finding:** Loom does **not reduce** total complexity — it
**relocates and re-implements** it. The thin client (~14k LOC) is only thin
because a ~232k-LOC Go daemon now carries the device-profile, paramset, and
classification logic that aiohomematic does in-process. In exchange Loom buys a
**cleaner wire model** (compact BIN-RPC south-bound, delta-only JSON over an
outgoing WebSocket north-bound, no inbound callback server) at the cost of an
**additional stateful, version-coupled daemon** as a new single point of failure
with its own operational surface.

**Headline scores** (full breakdown in §11):

- **As the HA backend *today*:** `aiohomematic` **9/10**, Loom **5/10**
  (Loom is disabled and not yet feature-equivalent).
- **As an architectural *approach* / future potential:** `aiohomematic` **7/10**,
  Loom **8/10** (the split is the better long-term design; daemon-side parity gaps
  are now largely closed in daemon API 1.18.0, leaving client consumption and the
  operational/SPOF cost to accept).
- **Network traffic (quality & quantity):** `aiohomematic` **6/10**, Loom
  **9/10** (in the canonical on-CCU deployment).

---

## 2. `aiohomematic` architecture (direct CCU)

A defensively engineered, in-process library. Layered into `client/` (transport),
`central/` (orchestration), `interfaces/` (Protocol/ABC contracts), `model/`
(~24k LOC — the device/data-point domain), `store/` (persistence + dynamic
caches), plus cross-cutting `metrics/`, `tracing.py`, `converter.py`, `schemas/`,
`rega_scripts/`.

**Transport — three protocols, two stacks:**

- **XML-RPC, outbound** (device ops: `setValue`, `getParamset`,
  `getParamsetDescription`, `listDevices`, `ping`, `init`): stdlib
  `xmlrpc.client.ServerProxy` — **blocking**, wrapped in a `ThreadPoolExecutor`
  (`client/rpc_proxy.py:8,25,34`). No native async XML-RPC.
- **JSON-RPC, outbound** (metadata: sysvars, programs, rooms, functions, names,
  firmware, ReGa scripts): `aiohttp` against `/api/homematic.cgi`
  (`client/json_rpc.py`, `const.py:315`).
- **XML-RPC, inbound (callback)**: a **local aiohttp server**
  (`AsyncXmlRpcServer`, `central/rpc_server.py:494`) listening on `0.0.0.0`
  (`const.py:289`) that the CCU calls back with `event`, `newDevices`,
  `deleteDevices`, etc. Registration via XML-RPC `init(callback_url,
  interface_id)` (`client/backends/ccu.py:382-384`). **BIN-RPC is not
  implemented.**

Per active interface there are up to three endpoints (write proxy, read proxy,
shared JSON-RPC session) — `client/backends/ccu.py:60-103`.

**Push vs. polling.** Device state is **pure push**: the CCU batches value
changes into `system.multicall` and POSTs them to the local callback server
(`central/rpc_server.py:157-193,285-304`). Polling is limited to liveness and hub
metadata (scheduler defaults, `central/scheduler.py:178-231`, `const.py:186-229`):

| Task | Interval |
|---|---|
| Connection checker (sends PING) | **15 s** |
| Periodic refresh (poll-only interfaces) | **15 s** |
| Sysvar / program / message poll (JSON-RPC) | **30 s** |
| Metrics / connectivity | **60 s** |
| Firmware-updating check | **5 min** |
| Firmware-delivery check | **1 h** |
| System-update check | **4 h** |
| Device-firmware check | **6 h** |

PING is issued by the 15 s connection checker (`client/interface_client.py:259-280`);
the CCU answers with a `PONG` event. Mismatch TTL 300 s, silence warning at 180 s.

**Startup.** Load disk cache (device + paramset descriptions, schema-versioned,
`store/persistent/`); `init` per interface; then the expensive
**O(devices × paramsets)** `getParamsetDescription` pass
(`client/interface_client.py:436`) — coalesced (`client/request_coalescer.py`) but
**not** batched via outbound multicall (outbound multicall is unused). Initial
values are pulled in **one bulk ReGa-script call per interface**
(`FETCH_ALL_DEVICE_DATA`, `json_rpc.py:930`) rather than N `getValue` calls — the
key startup optimization. Descriptions are cached to disk; values are always
re-fetched.

**Robustness.** Staged recovery pipeline (COOLDOWN → TCP → RPC → WARMING_UP →
STABILITY_CHECK → RECONNECT → DATA_LOADING → RECOVERED) with exp. backoff 5→60 s
(`central/coordinators/connection_recovery.py`); per-proxy circuit breakers
(5 fail → OPEN, 30 s reset, `client/circuit_breaker.py`); unified health score
(`central/health.py`); JSON-RPC session renew (≥90 s, `JSON_SESSION_AGE`);
command retry with backoff + jitter for transient CCU faults
(`client/command_retry.py`).

**Assessment.** Extremely mature, battle-tested, self-contained — one moving
part, no extra deployment. The price is high in-process complexity (several
overlapping state machines, very large modules — `client/json_rpc.py` ~98 KB,
`const.py` ~79 KB) and the inherent friction of XML-RPC: verbose payloads and a
**required inbound listener**, which is the source of most NAT/firewall pain.

---

## 3. OpenCCU-Loom architecture (daemon + thin client)

### 3.1 The daemon (`openccu-loom`, ~232k LOC Go, v0.7.1, API 1.17.0)

A Go port of aiohomematic's core plus a standalone "north-bound" surface. It
**owns** the CCU connection and re-implements the heavy logic server-side
(hexagonal design, in-process EventBus, `SPECIFICATION.md:243-303`). LOC by area
(tests excluded):

| Area | LOC | Content |
|---|---|---|
| `internal/north/` | 73,384 | REST/WS (17,830), MQTT (11,557), **Matter (41,445)** |
| `internal/model/` | 49,287 | 139 device profiles, 8 custom-DP types, typing |
| `internal/central/` | 35,407 | orchestration, hydration, caching, jobs |
| `internal/client/` | 15,956 | south-bound transport + reliability |
| `internal/store/` | 9,387 | SQLite persistence |

**South-bound (to CCU) — three wire protocols, BIN-RPC native:**

- **BIN-RPC** (binary over raw TCP): own codec, magic `{'B','i','n'}`, 8-byte
  header, typed values (`internal/client/transport/binrpc/wire.go:47-48`,
  `doc.go:4-12`). Used natively for CUxD — a deliberate divergence from
  aiohomematic, which routes CUxD via a JSON-RPC facade + MQTT workaround
  (`README.md:272`, `SPECIFICATION.md:322-325`). BIN-RPC is **~3–5× more compact**
  than XML-RPC (no tag overhead, typed binary values).
- **XML-RPC** (HmIP-RF, BidCos-RF/-Wired, VirtualDevices).
- **JSON-RPC** (ReGa hub scan).

The daemon hosts its own callback servers (XML-RPC `:8120` path-routed
`/RPC2/<central>`, BIN-RPC `:8129` envelope-routed), re-advertised to the CCU on
every `init`/reconnect so it is ephemeral-port tolerant
(`SPECIFICATION.md:305-325`). South-bound reliability defaults
(`pkg/hmreliability/`) are **CI-drift-tested against aiohomematic**
(`TestRecordedReliabilityDefaults`): connection checker 15 s, callback freshness
180 s, ping-pong TTL 300 s, circuit breaker 5/30 s/2.

**North-bound (to HA) — REST + WebSocket under `/api/v1`** (OpenAPI 3.1,
~90+ endpoints):

- **Bulk/snapshot:** `GET /snapshot` (single JSON or `x-ndjson` stream,
  `?include=channels|data_points`), `POST /devices/values:batch` (≤1000 DPs).
- **Reload (new in 0.7.1):** `POST /devices/{addr}/reload`,
  `.../channels/{no}/reload`, `POST /devices/refresh`.
- **WebSocket event stream** `GET /events`: envelope
  `{seq, kind, topic, type, ts, payload}` (`assets/wsapi.json:3-12`), **delta-only**
  push (value-change payload ~300–400 B, `previous`/`category` `omitempty`),
  ~17 broadcast types, server heartbeat **30 s**, read timeout 60 s. Resume via
  monotonic `seq` + ring buffer (1024), `subscribe{since:N}` → replay or
  `replay_lost` → client re-snapshots (ADR 0022).

**Extra surfaces are opt-in and share the CCU connection** (no extra radio
traffic): MQTT (`north.mqtt.enabled: false` by default), Matter
(`north.matter.enabled: false`). Both are north-bound adapters on the **same
in-process EventBus** — they do not open a second CCU link.

### 3.2 The thin client (`openccu-loom-client`, ~14k LOC Python)

Consumes the daemon over **one persistent outgoing WebSocket** (events) + **REST**
(commands, snapshot, refresh) against one port/auth family (Basic / Bearer /
Session, `auth.py`; Bearer is in-band rotatable without reconnect). **No inbound
callback server is needed** — the single biggest operational advantage over
XML-RPC, and it works behind NAT/firewalls.

The `compat/aiohomematic` layer is **surface-only** (`compat/aiohomematic/__init__.py:13-16`):
re-exported wire enums, an adapter façade (`central/adapter.py`, 1,406 LOC, aliased
to `CentralUnit`), real subclassing of Loom domain classes for `isinstance`
dispatch (`generic/__init__.py:202`, `custom/__init__.py:123`), and protocol-stub
mixins (`_protocol_surface.py`) to satisfy aiohomematic's `@runtime_checkable`
protocols.

**Complexity relocation — confirmed by the wire contract.** The daemon ships
**finished verdicts** the client never re-derives:
`DataPointSummary.category` ("the daemon derives internally … instead of
re-deriving categories from raw paramsets", `openccu_loom_types/rest.py:437-440`),
`.usage` (visibility verdict, `rest.py:445-448`), `CustomDPSummary.capabilities`
("mirrors the per-category Capability struct from `internal/model/custom/mixins.go`",
`rest.py:72-99`), plus sub-device split, grouping, room resolution, localized
labels.

**Important nuance — it is *re-hosting*, not a clean break.** The client still
**runs the real aiohomematic library** for: the routing-key algorithm
(`canonical.py:39-43` calls `aiohomematic.model.support.generate_unique_id`, the
Go side reproduces it bit-identically), the real `EventBus` + event classes
(HA entities subscribe on aiohomematic's own bus; the adapter republishes real
aiohomematic events, `refresh.py`), the `DeviceProfileRegistry` for naming
(`naming.py:31,159`), and climate enums. The client also locally reconstructs
naming composition, enum→option resolution, week-profile/schedule assembly, and
**polls hub singletons every 30 s** (`adapter.py:1121-1128`) because the daemon
has no push channel for them yet — the one remaining polling island in the client.

**Maturity of the client:** clean and production-shaped — **zero**
`NotImplementedError`/`TODO`/`FIXME` (grep-verified); the ~13 gaps are
**deliberate neutral-default stubs** with docstrings (light color/effect state,
text-display options, writable sysvars require an "extended" marker the daemon
doesn't emit yet) that **degrade silently rather than crash**.

---

## 4. Network topology — the decisive difference

```
aiohomematic (direct):
   ┌────────────────────────── LAN ──────────────────────────┐
   │                                                          │
   │  Home Assistant host                         CCU / OpenCCU
   │  ┌───────────────────────┐                  ┌──────────┐
   │  │ aiohomematic           │ ──XML-RPC out──▶ │          │
   │  │  + LOCAL XML-RPC        │ ──JSON-RPC────▶ │   ReGa   │
   │  │    CALLBACK SERVER ◀────┼──multicall push─┤   + RF   │
   │  └───────────────────────┘                  └──────────┘
   │   (CCU must reach BACK into HA — inbound listener)
   └──────────────────────────────────────────────────────────┘

OpenCCU-Loom (daemon co-located on the CCU — the canonical mode):
   ┌──────────── LAN ────────────┐   ┌──── loopback (127.0.0.1) ────┐
   │ Home Assistant               │   │  OpenCCU                     │
   │ ┌─────────────────────────┐  │   │ ┌────────┐    ┌──────────┐  │
   │ │ openccu-loom-client      │  │   │ │ loom   │XML/│          │  │
   │ │  (outgoing WS + REST) ───┼──┼──▶│ │ daemon │BIN─│   ReGa   │  │
   │ │  NO inbound listener ◀───┼──┼───┤ │        │◀───┤   + RF   │  │
   │ └─────────────────────────┘  │   │ └────────┘RPC └──────────┘  │
   └──────────────────────────────┘   └──────────────────────────────┘
        compact delta JSON / WS            compact BIN-RPC, on-box
```

- **`aiohomematic`:** one logical hop, but it requires HA to **host an inbound
  XML-RPC callback server** the CCU dials back into. This is the architectural
  root of NAT/container/firewall friction (`CallbackHostFor` problems, port
  binding, `0.0.0.0` listener).
- **Loom, daemon on the CCU** (first-class, packaged as a CCU/RaspberryMatic
  add-on pointing at `127.0.0.1`, `packaging/ccu-addon/README.md:14-17`;
  `internal/central/adapter/ccu_wiring.go:70-76`): the **expensive CCU hop
  becomes loopback** and uses compact BIN-RPC; only the lean delta-JSON WS/REST
  crosses the LAN, and **only outbound from HA**.
- **Loom, daemon separate from the CCU** (HA add-on / Docker): the south-bound
  hop is back on the LAN, so the LAN now carries *both* hops. Loom's net traffic
  advantage shrinks to "BIN-RPC is more compact than XML-RPC + no inbound
  listener" rather than "the radio hop is free."

---

## 5. Push / event model

| | `aiohomematic` | Loom |
|---|---|---|
| Delivery | CCU → local callback server (inbound) | Daemon → client (outbound WS) |
| Inbound listener required | **Yes** | **No** |
| Batching | CCU `system.multicall` | per-event delta frames |
| Resume after reconnect | re-`init`, reload data | `seq`-cursor replay → `replay_lost` re-snapshot |
| NAT/firewall friendly | No | **Yes** |
| Heartbeat | PING every 15 s | WS ping every 30 s (daemon-driven) |

Both deliver device state as push (good). Loom's advantage is purely structural:
an outgoing WebSocket needs no inbound port, survives NAT, and carries a
`seq`-based resume contract.

---

## 6. Startup / initial data load & caching

- **`aiohomematic`:** disk cache of device + paramset descriptions
  (schema-versioned, `store/persistent/`); expensive **O(devices × paramsets)**
  `getParamsetDescription` on cold start; **bulk** value fetch via
  `FETCH_ALL_DEVICE_DATA` ReGa script (one call/interface). Restart is fast when
  the schema matches (descriptions cached; values always re-fetched).
- **Loom client:** `GET /snapshot` returns devices + programs + sysvars in **one
  call**, but is followed by an **N×M REST fan-out** (per device, per channel for
  channels/DPs/CDPs) — a known scaling hotspot; a streaming snapshot is a
  "deferred ask" (`client.py:188-207`).
- **Loom daemon:** persistent **SQLite** VALUES/MASTER cache; warm boot does
  `restoreValuesFromCache` with **zero radio reads**, then a live
  `fetch_all_device_data`, then publishes north-bound (`docs/caching.md:60-70`).
  The daemon also makes the *un-ignore* of hidden parameters live-toggleable via
  REST without a restart, where aiohomematic requires a restart (ADR 0014).

**Net:** aiohomematic's cold-start cost lives in the HA process; Loom moves the
heavy hydration into the daemon (with a strong warm-start cache) but currently
pays an N×M REST fan-out between daemon and client on the first connect.

---

## 7. Complexity distribution

| | `aiohomematic` | Loom |
|---|---|---|
| Lines in the HA process | ~74,130 (full library) | ~14,000 (thin adapter) |
| Lines total in the system | ~74,130 | ~14,000 + ~2,479 + **~231,923 (daemon)** |
| Heavy logic location | in-process | in the Go daemon |
| Moving parts | 1 | 3 (daemon, client, types) + SQLite |
| Language(s) | Python | Go (daemon) + Python (client) |

This is the crux: **Loom's thinness in HA is bought with a much larger total
system.** The classification/profile logic (139 profiles, 8 custom-DP types,
paramset interpretation, capabilities, sub-device split, localization,
normalization, calculated DPs) moved from in-process Python into ~232k LOC of Go.
That is a sound engineering trade *if* you value a small HA footprint, a
language better suited to a long-running daemon, and reuse across non-HA
consumers (MQTT/Matter/Web-UI) — but it is not a complexity *reduction*.

---

## 8. Integration abstraction quality

The integration abstracts both backends behind aiohomematic's **`CentralUnit`**
Protocol. Quality is high and deliberate:

- **One shared interface**, no `if loom` sauce threaded through entities. Only
  **~11 real branch sites** total (3 in `control_unit.py`, 4 in `__init__.py`,
  4 in `config_flow.py`).
- **`backend_types.py`** resolves the one structural friction: aiohomematic's
  Protocol metaclass blocks both subclassing and `ABCMeta.register`, so platform
  dispatch uses `isinstance` tuples pairing each aiohomematic class with its Loom
  twin, degrading to the aiohomematic class alone on a CCU-only install
  (`backend_types.py:55-67`). Used by 7 platforms.
- **Polymorphism instead of branching** elsewhere: an `isawaitable` pattern for
  `get_paramset_description` (sync+cached on aiohomematic, async REST on Loom,
  `websocket_api.py:266-276`) and a `NotImplementedError` guard for event groups
  Loom doesn't model yet (`event.py:59-66`).

**Residual risk:** the duck-typed `cast(CentralUnit, …)` bridge is **not
statically type-checked**; drift between the aiohomematic API and the Loom twin
surfaces only at runtime, and `backend_types.py` must be hand-extended for every
new DP class.

---

## 9. Maturity & feature parity

- **`aiohomematic`:** the production default — 10/10 in this dimension.
- **Loom:** bundled but **disabled** (`LOOM_BACKEND_SELECTABLE = False`,
  `const.py:65`; `changelog.md` "not user-selectable in 2.8.0 … behaves as if it
  were absent"). UI/flow/i18n are fully prepared (zeroconf `_openccu-loom._tcp`,
  active mDNS browse, token flow, all strings in en/de).

**Where the parity gaps stand.** The catalogue was filed against the daemon as
[`docs/parity/ha-client-wire-gaps.md`](https://github.com/SukramJ/openccu-loom)
and then **code-verified against the daemon source** (openccu-loom 0.7.1,
**daemon API 1.18.0**, 2026-06-21). The verification both *closed* the genuine
daemon gaps and *reclassified* two items that were never daemon gaps. Status:

| Gap | Original root cause | Status (verified against daemon API 1.18.0) |
|---|---|---|
| Orphan-entity cleanup skipped (`control_unit.py:500-507`) | client/daemon — partial hub-coordinator surface | **Daemon closed** — `GET /hub/data-points` aggregates the singletons (alarm/service messages, inbox, metrics, connectivity, install-mode); client consumption pending |
| No per-device event groups (`event.py:62-65`) | client/daemon — `get_event_groups` raises | **Daemon closed (REST)** — `GET …/channels/{no}/event-groups`; WS variant deferred (bootstrap-once); client wiring pending |
| Text-display option lists empty (`custom/__init__.py:970-986`) | daemon — lists not serialized | **Daemon closed** — state now serializes all option lists (icons, sounds, bg/text colours, alignments, repetitions, intervals); client consumption pending |
| Hub-singleton push channel (30 s poll) | daemon — no push topic | **Daemon closed** — WS topics `hub.<central>.{alarm_messages,service_messages,inbox,metrics,connectivity.<id>}`; client can drop the poll loop |
| Light colour / effect read "unknown" (`custom/__init__.py:349-368`) | daemon — "not carried in wire state" | **Reclassified** — `color_temp_kelvin`/`effect` *are* serialized and read; only HS-colour is a `color:{h,s}` vs. flat `hue`/`saturation` **shape mismatch** — client-fixable |
| Writable sysvars downgraded (`hub/__init__.py:186-217`) | daemon — missing "extended" marker | **Withdrawn — not a gap** — `is_extended` is implemented end-to-end and **already read by the client** (`hub/__init__.py:225`); a read-only symptom points at the CCU description, not a missing field |
| Generic `set_on_time` no-op (`generic/__init__.py:215-227`) | unknown side | **Reclassified — client wiring** — daemon exposes `ON_TIME` via the generic value route |
| Reduced advanced settings (`config_flow.py:753-777`) | — | **By design** — callbacks/MQTT/pacing/interfaces are the daemon's concern, configured per-central |
| Trimmed options menu (`config_flow.py:1789`) | — | **By design** — daemon owns interfaces + program/sysvar scan |

**This revises the earlier "predominantly daemon-side" reading.** The four real
daemon gaps are now closed in daemon 0.7.1 / API 1.18.0, and two items that the
client's stubs *blamed on the daemon* (light colour/effect, writable sysvars)
turned out to be already-implemented or a client-side shape fix — the client's
own `"the daemon does not surface … yet"` comments were stale. The remaining work
has therefore shifted from **daemon-side exposure** to **client-side
consumption**: read the new G1 `color`/`color_mode`, consume `/hub/data-points`,
`/event-groups` and the new hub push topics, wire `set_on_time`, and flip
`LOOM_BACKEND_SELECTABLE`. (Caveat: verified at the source level; the installed
client `2026.6.21` / types `0.1.22` already reads `is_extended` and
`color_temp_kelvin`/`effect`, but does not yet consume the brand-new
1.18.0 endpoints.)

---

## 10. Robustness & operational risk

Both are robust on the wire (staged recovery + circuit breakers on aiohomematic;
`seq`-resume + replay + circuit breakers on Loom). The difference is the **risk
surface**:

| Risk | `aiohomematic` | Loom |
|---|---|---|
| Single point of failure | CCU only | **+ daemon** (no HA↔CCU bypass if daemon down) |
| State store | disk JSON caches | **SQLite** holding secrets, tokens, cache, history, Matter fabrics (corruption = multi-subsystem) |
| Multi-CCU blast radius | per-entry | 1 daemon for N CCUs → crash takes **all** offline (ADR 0002) |
| Version coupling | library ↔ HA core | **triple:** client ↔ `openccu_loom_types` ↔ daemon (`schema_digest`/`api_version`); digest mismatch is **warning only** → possible silent field errors |
| Secret loss | n/a | `secret.key` loss = secrets permanently undecryptable |
| Operational footprint | none extra | daemon deploy/update, DB backup, key mgmt, auth/OIDC, health/metrics |

Mitigations on the Loom side: single static Go binary, supervised fast restart
(monit/s6), warm-start SQLite cache, per-interface circuit-breaker isolation,
CI-enforced contract versioning (ADR 0028).

---

## 11. Scoring (1–10)

Two columns matter and are scored separately, because conflating "today's
shipping reality" with "the architecture on its merits" would be misleading.

### 11.1 Per-dimension

| Dimension | `aiohomematic` | Loom | Why |
|---|---:|---:|---|
| Network efficiency (quality) | 6 | **9** | BIN-RPC + delta WS + loopback vs. verbose XML-RPC + inbound server |
| Network footprint (quantity) | 6 | **8** | 9 when daemon on-CCU; ~7 when daemon separate (both hops on LAN) |
| NAT / firewall friendliness | 4 | **9** | outgoing WS only vs. required inbound callback listener |
| Startup performance / scalability | 7 | 6 | aiohomematic disk-cache + bulk fetch vs. client N×M fan-out (daemon warm-start is strong, 8) |
| HA-process footprint | 5 | **9** | 74k in-process vs. ~14k thin adapter |
| Total system complexity | **7** | 4 | one library vs. daemon (232k Go) + client + types + SQLite |
| Integration abstraction cleanliness | — | **8** | clean `CentralUnit` façade, ~11 branch sites (aiohomematic *is* the interface) |
| Maturity / production readiness (in HA) | **10** | 4 | default backend vs. disabled groundwork (daemon now parity-complete; HA backend still gated off) |
| Robustness / reconnect | **9** | 8 | both strong; Loom carries daemon SPOF |
| Operational simplicity | **9** | 5 | no extra deployment vs. daemon lifecycle, DB, secrets |
| Feature completeness / parity | **10** | 7 | daemon-side gaps closed (API 1.18.0); remaining is client consumption |
| Extensibility / ecosystem | 6 | **9** | HA-only library vs. MQTT + Matter + REST + Web-UI, multi-consumer |

### 11.2 Overall

| Verdict | `aiohomematic` | Loom |
|---|---:|---:|
| **As the HA backend today** | **9 / 10** | **5 / 10** |
| **As an architectural approach (future)** | **7 / 10** | **8 / 10** |

**Reading:** aiohomematic wins decisively *right now* — it is mature, complete,
self-contained, and shipping. Loom is the stronger long-term *architecture*
(thin HA footprint, NAT-friendly, efficient wire, multi-consumer ecosystem). The
daemon-side parity gaps are now largely closed (daemon API 1.18.0), so realizing
that score has shifted from a daemon problem to **client-side consumption** of
the new wire surface, accepting the daemon's operational/SPOF costs, and actually
enabling the backend.

---

## 12. Network traffic assessment (quality & quantity)

This is the dimension where Loom is most clearly superior — with one important
caveat about deployment topology.

### 12.1 Quality

- **`aiohomematic`:** a **mixed, verbose** profile. XML-RPC carries heavy textual
  tag overhead; the model **requires an inbound callback server** in the HA host
  (the dominant *qualitative* weakness — it dictates network placement, breaks
  under NAT/containers, and needs a bound `0.0.0.0` port). State is push, but hub
  metadata is polled.
- **Loom:** a **clean, modern** profile. South-bound BIN-RPC is a compact,
  typed binary frame (~3–5× smaller than XML-RPC) and, in the canonical
  deployment, runs over loopback. North-bound is **delta-only JSON** over a
  **single outgoing WebSocket** with a `seq`-based resume contract — no inbound
  listener, NAT-friendly, payloads ~300–400 B with optional fields elided.
  **Quality verdict: Loom clearly ahead.**

### 12.2 Quantity

Steady-state, idle system:

| Traffic class | `aiohomematic` (LAN) | Loom on-CCU | Loom separate |
|---|---|---|---|
| Liveness | PING every **15 s × interfaces** + PONG | WS ping every **30 s** (1 conn) | same 30 s |
| Hub metadata | sysvar/program/message poll every **30 s** (scales with sysvar count) | **30 s** hub-singleton poll (few fixed endpoints) | same |
| Device state | XML-RPC multicall push (verbose XML) | delta JSON push (compact) | compact + south-bound BIN-RPC on LAN |
| Inbound server | required | none | none |
| CCU hop on LAN | **yes** (all of the above) | **no** (loopback) | **yes** (BIN-RPC) |

- **`aiohomematic`:** idle LAN traffic is dominated by the **30 s sysvar/program
  poll** (volume scales with hub configuration) plus a 15 s PING per interface;
  device events add load only on actual change. All of it crosses the LAN, in
  verbose XML.
- **Loom, daemon on the CCU:** the heavy south-bound chatter (polls, pings,
  paramset traffic, value events) is **loopback and free of LAN cost**; the LAN
  sees only a lean outgoing WS (30 s heartbeat + deltas). The last 30 s
  hub-singleton poll is now eliminable too — daemon API 1.18.0 adds hub push
  topics, so once the client subscribes to them the steady state is push-only.
  **Substantially less LAN traffic, fewer connections, no inbound port.**
- **Loom, daemon separate from the CCU:** the south-bound hop returns to the LAN,
  so total LAN bytes ≈ both hops. Loom still wins on *quality* (BIN-RPC compactness,
  no inbound listener) but the *quantity* advantage narrows.

**Bandwidth note — Matter/MQTT do not add CCU/radio traffic** (they fan out the
same in-process EventBus) and are opt-in; enabling them adds only their own
north-bound traffic.

### 12.3 Network verdict

- **Quality:** Loom **9/10** — compact binary south-bound, delta JSON north-bound,
  no inbound listener, resumable. aiohomematic **6/10** — verbose XML + a required
  callback server.
- **Quantity:** Loom **9/10 on-CCU** / **~7/10 when separate**; aiohomematic
  **6/10** — constant 15 s/30 s polling across the LAN in verbose XML.

---

## 13. Bottom line

- **Today, ship and trust `aiohomematic`.** It is the mature, complete,
  self-contained backend; Loom is correctly gated off.
- **Loom is the better long-term wire architecture** — especially for network
  traffic and NAT/firewall friendliness when the daemon is co-located on the CCU,
  and for reaching beyond Home Assistant (MQTT, Matter, REST, Web-UI).
- **Loom does not reduce complexity; it relocates it** into a large, stateful,
  version-coupled Go daemon that becomes a new SPOF with real operational cost.
  The integration-side abstraction is clean and low-risk.
- **The remaining work is now client-side, not daemon-side.** As of daemon
  0.7.1 / API 1.18.0 the real daemon parity gaps are closed (hub data-points,
  event-groups, text-display options, hub push topics), and two suspected daemon
  gaps were already-implemented or a client shape fix. What is left before
  flipping `LOOM_BACKEND_SELECTABLE` is a defensible product decision: have the
  Python client consume the new 1.18.0 wire surface, accept the daemon's
  operational/SPOF costs, and enable the backend.
