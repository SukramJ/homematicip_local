# Homematic(IP) Local 2.0.0 - Release Notes

This release brings numerous improvements for daily use, from a redesigned setup experience to new control options for sirens and dimmers.

---

## Easier Setup and Configuration

### New Reauthentication Flow

When your CCU password has changed or credentials have expired, you no longer need to delete and re-add the integration. Home Assistant will display a "Reauthenticate" button that allows you to simply enter the new credentials.

### Quick Reconfiguration

The new "Reconfigure" option in the integration settings allows you to quickly adjust connection settings (host, port, TLS) without repeating the entire setup process. Useful when your CCU moves to a new IP address.

### Improved Error Messages

Configuration steps now show "Step X of Y" so you know how far along the setup has progressed. Error messages have been redesigned with specific hints about what to check - whether the CCU is reachable or if credentials are correct.

---

## CCU Backup from Home Assistant

### Create Backups Without Leaving Home Assistant

You can now create CCU system backups directly from Home Assistant using the new backup service. No need to log into the CCU web interface.

**How to create a backup:**

```yaml
service: homematicip_local.create_backup
data: {}
```

The backup file will be stored on your CCU and can be downloaded from there. This is useful for:
- Regular automated backups via Home Assistant automations
- Creating a backup before making configuration changes
- Disaster recovery preparation

**Example: Weekly backup automation:**

```yaml
automation:
  - alias: "Weekly CCU Backup"
    trigger:
      - platform: time
        at: "03:00:00"
    condition:
      - condition: time
        weekday:
          - sun
    action:
      - service: homematicip_local.create_backup
```

---

## Device Pairing Made Easy

### Install Mode Control

Pairing new devices is now easier with dedicated install mode controls directly in Home Assistant. The integration provides separate buttons for each interface:

| Entity | Function |
|--------|----------|
| **Activate Install Mode HmIP-RF** | Start pairing mode for HomematicIP devices |
| **Activate Install Mode BidCos-RF** | Start pairing mode for classic Homematic devices |

### Install Mode Duration Sensors

Two sensors show the remaining time while install mode is active:

- **Install Mode HmIP-RF duration**: Countdown for HomematicIP pairing (in seconds)
- **Install Mode BidCos-RF duration**: Countdown for BidCos pairing (in seconds)

When the sensor shows 0, install mode has ended.

**Example: Start pairing and notify when ready:**

```yaml
automation:
  - alias: "Start HmIP Pairing"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: START_PAIRING
    action:
      - service: button.press
        target:
          entity_id: button.ccu_activate_install_mode_hmip_rf
      - service: notify.mobile_app
        data:
          message: "Install mode active for 60 seconds. Pair your device now!"
```

---

## Adding New Devices from the Inbox

### Delayed Device Creation via Repairs

When you pair a new device with your CCU, it first appears in the CCU's "inbox" waiting to be accepted. Previously, you had to use the CCU web interface to accept these devices. Now Home Assistant handles this for you.

### How It Works

1. **Pair the device** with your CCU (using install mode)
2. **A repair notification** appears in Home Assistant's Settings → System → Repairs
3. **Click the repair** to see the pending device
4. **Enter a name** for the device (or leave empty for the default)
5. **Confirm** to add the device to Home Assistant

### What You'll See

The repair notification shows:
- Device address (e.g., `000A1B2C3D4E5F`)
- Interface (HmIP-RF or BidCos-RF)
- A text field to enter your preferred device name

### Inbox Sensor

A new **Inbox** sensor shows how many devices are waiting in the CCU inbox. This makes it easy to:
- Monitor for newly paired devices
- Create automations that notify you when devices are pending

```yaml
automation:
  - alias: "Notify on New Inbox Device"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ccu_inbox
        above: 0
    action:
      - service: notify.mobile_app
        data:
          message: "New device in CCU inbox - check Repairs to add it"
```

---

## Siren Control Without Workarounds

### Automatic Select Entities for Tone and Light Pattern

Sirens like HmIP-ASIR now automatically provide two select entities:

- **Siren Tone**: Choose the acoustic alarm tone (rising, falling, alternating, etc.)
- **Siren Light Pattern**: Choose the optical alarm pattern (blinking, alternating, etc.)

These entities can be used directly in automations - no need to manually create InputHelper entities anymore. The selected values are used as defaults when the siren is activated without explicit parameters.

**Example Automation:**

```yaml
- service: select.select_option
  target:
    entity_id: select.living_room_siren_siren_tone
  data:
    option: "Rising frequency"

- service: siren.turn_on
  target:
    entity_id: siren.living_room_siren
```

---

## Dimmers Remember Their Last Brightness

### Restore Last Brightness

Dimmers now save their last brightness setting and automatically restore it when turned on - even after a Home Assistant restart.

**In practice this means:**
- Set dimmer to 40% → turn off → turn on → dimmer is back at 40%
- Works with all dimmers (HmIP-BDT, HmIP-PDT, etc.)
- The setting survives Home Assistant restarts

If you want a different brightness, simply specify it explicitly when turning on.

---

## System Monitoring at a Glance

### New Diagnostic Sensors

Three new sensors show the state of your CCU connection:

| Sensor | Description |
|--------|-------------|
| **System Health** | Overall connection health (0-100%) |
| **Connection Latency** | CCU response time in milliseconds |
| **Last Event Age** | Seconds since the last received CCU event |

These sensors are great for:
- Monitoring dashboards
- Notifications when connection issues occur
- Long-term analysis of connection quality

---

## New Device Support

### HmIP-WRCD - Wall-Mount Remote Control with Display

The wall-mount remote with display can now show text, icons, and colors:

```yaml
- service: notify.homematicip_local
  data:
    message: "Heating on"
    target: "HmIP-WRCD-000000"
    data:
      icon: "sun"
      color: "orange"
      sound: "long_short"
```

### HmIP-MP3P - Combination Signalling Device

Full support for the combination signalling device with MP3 playback and RGB LED:

- **Play sounds**: `play_sound` service with volume and repeat options
- **Control LED**: `set_sound_led` service with color, brightness, and blink patterns
- **Stop sounds**: `stop_sound` service

---

## Improved Connection Stability

### Automatic Recovery After CCU Restart

The integration now more reliably detects when the CCU has restarted and automatically restores the connection. The recovery process has been improved:

- Staged connection verification
- Automatic retry attempts with backoff
- Fewer error messages in the log during recovery

### Less Log Spam During Connection Issues

Temporary connection problems no longer flood the log with error messages. Instead, a summary is provided when issues occur and when they are resolved.

---

## Easier Schedule Management

### Simplified Schedule Format

Heating schedules can now be read and written in a simpler format, making heating automation more straightforward.

### Faster Schedule Operations

Schedules are cached, making repeated queries much faster.

---

## Minor Improvements

- **Air Quality Sensors**: New entities for DIRT_LEVEL and SMOKE_LEVEL
- **Translations**: Improved translations for entities and error messages

---

## Bug Fixes

- Service `set_schedule_simple_weekday` works correctly again
- Covers and dimmers no longer remain "unavailable" after CCU restart
- RGBW lights no longer turn off unexpectedly during transitions
- Firmware updates are correctly refreshed after checking

---

## Call for Testers: Async XML-RPC Server (Experimental)

We have developed a new **asyncio-native XML-RPC server** as an alternative to the current thread-based implementation. This experimental feature may improve performance and resource usage, especially on systems with many devices.

### What's Different?

The new async server:
- Runs entirely within the asyncio event loop (no extra threads)
- Supports batched CCU events via `system.multicall`
- Includes a health-check endpoint for monitoring
- Provides detailed metrics (request count, latency, errors)

### How to Enable It

1. Go to **Settings → Devices & Services → Homematic(IP) Local**
2. Click **Configure** on your integration
3. Select **Debug and Analysis Settings**
4. Enable **Use async XML-RPC server**
5. Click **Submit**
6. Restart Home Assistant for the change to take effect

### What to Watch For

When testing, please pay attention to:

1. **Event Reception**: Do all device state changes arrive in Home Assistant?
2. **Latency**: Does the system feel responsive?
3. **Stability**: Any crashes or connection drops?
4. **Resource Usage**: CPU/memory compared to the default server
5. **Log Messages**: Any errors or warnings related to the RPC server?

### How to Report Issues

If you encounter any problems or have feedback, please:

1. Open an issue at [GitHub Issues](https://github.com/sukramj/aiohomematic/issues)
2. Include:
   - Your Home Assistant version
   - Number of Homematic devices
   - CCU type (CCU3, RaspberryMatic, etc.)
   - Relevant log entries (set `aiohomematic` logger to `debug` if needed)
   - Description of the issue

Even if everything works perfectly, we'd love to hear about your experience!

### How to Disable It

If you encounter issues, go back to **Debug and Analysis Settings** in the integration configuration, disable the option, and restart Home Assistant to return to the default thread-based server.

---

## Update Notes

This version requires:
- **Home Assistant 2025.10.0** or newer
- **Python 3.13** or newer

Configuration is automatically migrated. After updating, consider checking the diagnostic settings to enable the new system monitoring sensors.

---

# Version [2.0.0](https://github.com/SukramJ/homematicip_local/compare/1.90.2...2.0.0) (2026-01-02)

## What's Changed

### New Features

- **HmIP-WRCD Text Display**: Full support for the wall-mount remote control with display via NotifyEntity, including services for sending text with icons, colors, sounds, and alignment options
- **HmIP-MP3P Sound Player**: Full support for the combination signalling device with services for sound playback (play_sound, stop_sound) and LED control (set_sound_led) with colors, brightness, and timing options
- **Siren Control**: Automatic select entities for siren tone and light pattern selection with full translations (no manual InputHelper setup required)
- **Reauthentication**: Added reauthentication flow to update expired credentials without removing the integration
- **Reconfigure Flow**: Quick reconfiguration of connection settings without full re-setup
- **Air Quality Sensors**: New entity descriptions for DIRT_LEVEL and SMOKE_LEVEL sensors
- **Enhanced Diagnostics**: Comprehensive system metrics in diagnostics including RPC statistics, event bus metrics, cache performance, health status, and service call analytics
- **System Metrics Sensors**: New diagnostic sensors for monitoring system health (%), connection latency (ms), and last event age (s) - providing real-time visibility into CCU communication status
- **Delayed Device Repair**: Devices stuck in the CCU inbox can now be added through Home Assistant's repairs interface with a guided fix flow
- **Restore Last Brightness**: Dimmers now remember their last brightness level and automatically restore it when turned on without specifying brightness (persists across HA restarts)

### Improvements

- **Configuration Experience**: Enhanced config flow with improved error messages, progress indicators (Step X of Y), and menu-based navigation
- **Error Handling**: Reduced log flooding during connection issues with improved error handling decorator for entity actions
- **Translations**: Fixed naming of untranslated entities and improved translation coverage for press events
- **Translations**: Added missing repair issue translations (callback_server_failed, client_failed, connection_failed) and entity translations (button_press)

### Bug Fixes

- **Services**: Fixed `set_schedule_simple_weekday` service
- **Translations**: Fixed translation issues

### Developer Experience

- **Code Quality**: Strict mypy type checking, consistent use of keyword-only arguments, removed legacy code from config flow
- **Testing**: Comprehensive test coverage improvements for config flow, services, lights, and updates
- **Documentation**: Added comprehensive CLAUDE.md for AI assistants with development guidelines and project structure

## Bump aiohomematic to [2026.1.2](https://github.com/SukramJ/aiohomematic/compare/2025.11.7...2026.1.2)

### Storage & Persistence

- **Storage Abstraction Layer**: Unified storage system enabling Home Assistant Store integration
  - Protocol-based architecture allows transparent substitution of storage backends
  - Local implementation uses orjson for fast serialization with atomic writes
  - Supports ZIP archive loading, version migrations, and delayed/debounced saves
- **Device Definition Export**: Export device definitions as single ZIP file for easier sharing and debugging

### RPC Server

- **Async XML-RPC Server** (Experimental): New asyncio-native alternative to thread-based server
  - Enable via `OptionalSettings.ASYNC_RPC_SERVER` in CentralConfig
  - Full `system.multicall` support for batched CCU events
  - Health-check endpoint (`GET /health`) for monitoring
  - Metrics: request count, error count, latency, active background tasks
  - Graceful shutdown with task cancellation

### Connection Recovery

- **Unified Recovery Architecture**: New event-driven connection recovery coordinator
  - Staged recovery process: TCP check → RPC check → Warmup → Stability check → Reconnect
  - Automatic retry with exponential backoff (max 8 attempts)
  - Parallel recovery support for multi-interface setups
- **Fixed Authentication Errors**: JSON-RPC sessions are now cleared when recovery starts
  - Prevents "access denied" errors after CCU restarts
- **Device Inbox at Startup**: Inbox sensor now available immediately after integration start
- **Repair Issues Restored**: Delayed device creation again triggers repair issues in HA

### Observability & Metrics

- **Complete Event-Driven Metrics**: All components now emit metric events to EventBus instead of maintaining local state
  - `MetricsObserver` aggregates latency, counter, gauge, and health metrics in real-time
  - Type-safe `MetricKey` dataclass with `MetricKeys` factory for all known metrics
  - `emit_latency()`, `emit_counter()`, `emit_gauge()`, `emit_health()` functions for easy metric emission
  - Dedicated `aiohomematic/metrics/` module with clean separation of concerns
- **Comprehensive System Events**: New events for complete system observability
  - Connection state changes with reason tracking
  - Cache invalidation and refresh events
  - Circuit breaker state transitions and trip notifications
  - Scheduler task execution and data refresh events
  - Request coalescing events for performance monitoring
- **RPC Server Monitoring**: Track incoming requests from CCU with latency, error rates, and active tasks
- **Generic Serialization**: All metrics and health data now export to JSON-serializable dictionaries
- **Data Point Categories**: View data point counts grouped by type (SWITCH, SENSOR, CLIMATE, etc.)
- **Improved Cache Metrics**: Clear distinction between true caches (with hit/miss) and trackers (size only)
- **Self-Healing Recovery**: Automatic data refresh after circuit breaker recovery
- **Hub Metrics Sensors**: Three HA-visible sensors for real-time system monitoring:
  - System Health (0-100%)
  - Connection Latency (ms)
  - Last Event Age (seconds since last CCU event)
- **RPC Monitoring**: Track success/failure rates, latency, and request coalescing effectiveness

### Connection Reliability

- **Improved Reconnection**: New state machine architecture for faster, more reliable recovery after CCU restarts
- **CircuitBreaker**: Automatic protection against repeated connection failures with staged reconnection
- **Reduced Log Noise**: Less ERROR logging during expected reconnection scenarios

### Device Management

- **Device Inbox**: Accept and rename new devices pending pairing directly from the integration
- **Install Mode**: Separate install mode control per interface (HmIP-RF and BidCos-RF) with countdown timer
- **Backup Support**: Create and download CCU system backups, firmware download and update triggers

### Climate & Schedules

- **Schedule Caching**: Faster schedule operations with intelligent caching
- **Simple Schedule Format**: Easier to read and modify weekly heating schedules
- **Schedule Sync**: Bidirectional get/set schedule operations with filtered data format

### Siren Control

- **Visible Alarm Settings**: Acoustic and optical alarm selection now available as controllable entities
- **Flexible Turn-On**: Siren activation uses entity values as defaults when service parameters omitted

### Bug Fixes

- **Device Creation Race Condition**: Fixed startup crash when CCU callback and initialization code raced
- **Resilient Channel Handling**: Devices remain functional even when some channel descriptions are missing
- **Cover/Dimmer Restart**: Fixed `is_valid` returning False after CCU restart when status is UNKNOWN
- **Empty Numeric Values**: Fixed conversion error when CCU sends empty strings for FLOAT/INTEGER parameters
- **RGBW/LSC Auto-Off**: Fixed lights turning off unexpectedly when using transition times
- **Reconnect Availability**: Entities no longer remain unavailable after CCU reconnect
- **STATUS Parameters**: Fixed handling of integer values from backend for status updates
- **Firmware Updates**: Fixed firmware data not refreshing after update check

### New Device Support

- **HmIP-MP3P Kombisignalgeber**: Sound player with MP3 playback (channel 2) and RGB LED control (channel 6)
- **HmIP-WRCD Text Display**: Wall-mount Remote Control with Display - send text, icons, colors, and sounds to the LCD
- DeviceProfileRegistry for centralized device-to-profile mappings
- DpActionSelect data point type for write-only selection parameters

### Developer Experience

- **Fluent Configuration**: New `CentralConfigBuilder` with method chaining and factory presets for CCU/Homegear
- **Request Tracing**: Context variables pattern for request tracking through async call chains with automatic log prefixing
- **Type Converters**: Extensible `to_homematic_value()` / `from_homematic_value()` using singledispatch pattern

### Internal Improvements

- Protocol-based architecture for better testability and decoupling
- Event bus system replacing legacy callback patterns
- Strict type checking throughout codebase
- Translatable log messages and exceptions
- Generic protocols for improved mypy type inference on data point values
- Declarative field descriptors for custom and calculated data points
- `DelegatedProperty` descriptor for simple property delegation with caching support
- Enhanced linter with DP004 path validation for DelegatedProperty definitions
- Store package restructured into `persistent/` and `dynamic/` subpackages for better maintainability
- Typed dataclasses (`CachedCommand`, `PongTracker`) replace untyped tuples and dicts
- Event-driven test patterns with `EventCapture` fixture for behavior verification through events
- Import standardization with `lint-package-imports` pre-commit hook enforcing package facade usage
- Package structure refactoring: Split large `__init__.py` files into dedicated modules
  - `central/coordinators/` subpackage for CacheCoordinator, ClientCoordinator, ConnectionRecoveryCoordinator, DeviceCoordinator, EventCoordinator, HubCoordinator
  - `central/events/` subpackage for EventBus, event types, and integration events
  - `client/ccu.py`, `client/config.py` for client classes
  - `model/hub/hub.py` for Hub orchestrator
- Export validation with `lint_all_exports.py` ensuring consistent `__all__` exports
- **Semantic Naming**: Renamed classes to reflect actual purpose
  - `CommandCache` → `CommandTracker` (tracks sent commands, not a cache)
  - `PingPongCache` → `PingPongTracker` (tracks connection health)
  - `*DescriptionCache` → `*DescriptionRegistry` (authoritative stores)
  - `ParameterVisibilityCache` → `ParameterVisibilityRegistry`
- **TrackerStatistics**: Dedicated statistics class for trackers (evictions only, no hit/miss)
