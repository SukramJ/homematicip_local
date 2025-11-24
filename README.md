# Homematic(IP) Local for OpenCCU
[![releasebadge]][release] 
[![License][license-shield]](LICENSE.md) 
[![hainstall][hainstallbadge]][hainstall]
[![GitHub Sponsors][sponsorsbadge]][sponsors]
[![hacs][hacsbadge]][hacs]

Homematic(IP) Local for OpenCCU is a custom [integration](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) for Home Assistant.

## Quick start:

- Installation guide: https://github.com/sukramj/homematicip_local/wiki/Installation
- Alternative installation by J. Maus (OpenCCU): https://github.com/OpenCCU/OpenCCU/wiki/HomeAssistant-Integration
- Wiki (additional information): https://github.com/sukramj/aiohomematic/wiki
- Changelog: https://github.com/sukramj/homematicip_local/blob/master/changelog.md
- License: https://github.com/sukramj/homematicip_local/blob/master/LICENSE

Please support the community by adding more valuable information to the wiki.

## Other Homematic related integrations:

To connect to the Homematic IP Cloud (Access Point), please use the [Homematic(IP) Cloud](https://www.home-assistant.io/integrations/homematicip_cloud) integration.

To connect locally to your Homematic Home Control Unit (HmIP-HCU1), please use the [Homematic IP Local (HCU)](https://github.com/Ediminator/hacs-homematicip-hcu) integration.

## At a glance

- Local Home Assistant integration for Homematic(IP) hubs (CCU2/3, OpenCCU, Debmatic, Homegear). No cloud required.
- Communication: Local XML-RPC for control and push state updates; JSON-RPC for names and rooms.
- Installation: HACS recommended; manual installation supported.
- Auto-discovery: Supported for CCU and compatible hubs.
- Minimum requirements: Home Assistant 2025.8.0+; for Homematic IP on CCU require at least CCU2 2.53.27 / CCU3 3.53.26.
- Useful links: [Installation guide](https://github.com/sukramj/homematicip_local/wiki/Installation), [Wiki](https://github.com/sukramj/aiohomematic/wiki), [Issues](https://github.com/sukramj/aiohomematic/issues), [Discussions](https://github.com/sukramj/aiohomematic/discussions), [Changelog](https://github.com/sukramj/homematicip_local/blob/master/changelog.md).

## Table of contents
- [Issues and discussions](#issues-and-discussions)
- [Documentation](#documentation)
- [Installation](#installation)
- [Device support](#device-support)
- [Requirements](#requirements)
- [Configuration](#configuration)
  - [Manual configuration steps](#manual-configuration-steps)
  - [Auto-discovery](#auto-discovery)
  - [Configuration Variables](#configuration-variables)
- [System variables](#system-variables)
- [Actions](#actions)
- [Events](#events)
- [Additional information](#additional-information)
- [Updating a device firmware](#updating-a-device-firmware)
- [CUxD, CCU-Jack and MQTT support](#cuxd-ccu-jack-and-mqtt-support)
- [CUxD and CCU-Jack device support](#cuxd-and-ccu-jack-device-support)
- [Troubleshooting](#troubleshooting)
- [Frequently asked questions](#frequently-asked-questions)
- [Examples in YAML](#examples-in-yaml)
- [Available Blueprints](#available-blueprints)
- [Support and Contributing](#support-and-contributing)
- [License](#license)

## Issues and discussions

Please report issues in [aiohomematic repo](https://github.com/sukramj/aiohomematic/issues).
New discussions can be started and found in [aiohomematic repo](https://github.com/sukramj/aiohomematic/discussions).
Feature requests can be added as a discussion too.
A good practice is to search in issues and discussions before starting a new one.

## Documentation

Additional topics:
- Naming of devices and entities: docs/naming.md

The [Homematic](https://www.homematic.com/) integration provides bi-directional communication with your Homematic hub (CCU, Homegear etc.).
It uses an XML-RPC connection to set values on devices and subscribes to receive events the devices and the CCU emit.
You can configure this integration multiple times if you want to integrate multiple Homematic hubs into Home Assistant.

**Please take the time to read the entire documentation before asking for help. It will answer the most common questions that come up while working with this integration.**

## Installation

Recommended: HACS
- In Home Assistant, go to HACS > Integrations > Explore & Download Repositories.
- Search for "Homematic(IP) Local for OpenCCU" and install it.
- Restart Home Assistant when prompted.

Manual installation
- Copy the directory custom_components/homematicip_local from this repository to your Home Assistant config/custom_components directory.
- Restart Home Assistant.
- Attention: The method does not support updates.

After installation, proceed with configuration below via the Add Integration flow.

## Device support

Homematic and HomematicIP devices are integrated by automatically detecting the available parameters, for which suitable entities will be added to the corresponding device-object within Home Assistant.
However, for more complex devices (thermostats, some cover-devices and more) we perform a custom mapping to better represent the devices features. This is an internal detail you usually don't have to care about.
It may become relevant though if new hardware becomes available.
In such a case the automatic mode will be active. Therefore f.ex. a new thermostat-model might not include the `climate` entity.
In such a case you may report the missing customization in the [aiohomematic](https://github.com/sukramj/aiohomematic) repository.
Please report missing devices **after** you installed the integration and ensured it is missing or faulty.

### Deactivated Entities

A lot of additional entities were initially created _deactivated_ and can be _activated_, if necessary, in the `advanced settings` of the entity.

## Requirements

### Hardware

This integration can be used with any CCU-compatible Homematic hub that exposes the required XML-RPC interface. This includes:

- CCU2/3
- OpenCCU
- Debmatic
- Homegear
- Home Assistant OS / Supervised with a suitable add-on + communication device

Due to a bug in previous versions of the CCU2 / CCU3, this integration requires at least the following version for usage with Homematic IP devices:

- CCU2: 2.53.27
- CCU3: 3.53.26

### Firewall and required ports

To allow communication to your Homematic hub, a few ports on the hub have to be accessible from your Home Assistant machine. The relevant default ports are:

- BidCosRF (_old_ wireless devices): `2001` / `42001` (with enabled TLS)
- HomematicIP (wireless and wired): `2010` / `42010` (with enabled TLS)
- Homematic wired (_old_ wired devices): `2000` / `42000` (with enabled TLS)
- Virtual thermostat groups: `9292` / `49292` (with enabled TLS)
- JSON-RPC (used to get names and rooms): `80` / `443` (with enabled TLS)

Advanced setups might consider this:

This integration starts a local XML-RPC server within HA, which automatically selects a free port or uses the optionally defined callback port.
This means that the CCU must be able to start a new connection to the system running HA and to the port. So check the firewall of the system running HA (host/VM) to allow communication from the CCU. This Traffic (state updates) is always unencrypted.
If running HA on docker it is recommended to use `network_mode: host`, or specify the callback_host and callback_port_xml_rpc parameters (see [Configuration Variables](#configuration-variables)).

### Authentication

This integration always passes credentials to the Homematic hub when connecting.
For CCU and descendants (OpenCCU, debmatic) it is **recommended** to enable authentication for XML-RPC communication (Settings/Control panel/Security/Authentication). JSON-RPC communication is always authenticated.

The account used for communication is **required** to have admin privileges on your Homematic hub.
It is important to note though, that special characters within your credentials may break the possibility to authenticate.
Allowed characters for a CCU password are: `A-Z`, `a-z`, `0-9` and `.!$():;#-`.
The CCU WebUI also supports `ÄäÖöÜüß`, but these characters are not supported by the XML-RPC servers.

If you are using Homegear and have not set up authentication, please enter dummy-data to complete the configuration flow.

# Configuration

Adding Homematic(IP) Local for OpenCCU to your Home Assistant instance can be done via the user interface, by using this My button: [ADD INTEGRATION](https://my.home-assistant.io/redirect/config_flow_start?domain=homematicip_local)

## Manual configuration steps

- Browse to your Home Assistant instance.
- In the sidebar click on [Configuration](https://my.home-assistant.io/redirect/config)
- From the configuration menu select: [Integrations](https://my.home-assistant.io/redirect/integrations)
- In the bottom right, click on the [Add Integration](https://my.home-assistant.io/redirect/config_flow_start?domain=homematicip_local) button.
- From the list, search and select "Homematic(IP) Local for OpenCCU".
- Follow the instructions on screen to complete the setup.

## Auto-discovery

The integration supports auto-discovery for the CCU and compatible hubs like OpenCCU. The Home Assistant User Interface will notify you about the integration being available for setup. It will pre-fill the instance-name and IP address of your Homematic hub. If you have already set up the integration manually, you can either click the _Ignore_ button or re-configure your existing instance to let Home Assistant know the existing instance is the one it has detected. After re-configuring your instance a HA restart is required.

Autodiscovery uses the last 10 digits of your rf-module's serial to uniquely identify your CCU, but there are rare cases where the CCU API and the UPNP-Message contains/returns different values. In these cases, where the auto-discovered instance does not disappear after a HA restart, just click on the _Ignore_ button.
Known cases are in combination with the rf-module `HM-MOD-RPI-PCB`.

### Configuration Variables

The integration uses a multi-step configuration flow that guides you through all necessary settings. This section explains each configuration option in detail.

---

## Step 1: CCU Connection Settings

These are the basic settings required to connect Home Assistant to your Homematic hub.

### Required Settings

| Setting | Description | Example | Notes |
|---------|-------------|---------|-------|
| **Instance Name** | Unique identifier for this integration instance | `homematic_ccu3` | Use lowercase letters and numbers only (a-z, 0-9). Must be unique if connecting multiple HA instances to the same CCU or connecting to multiple CCUs. |
| **Host** | Hostname or IP address of your CCU | `192.168.1.50` or `ccu3.local` | Make sure your CCU has a static IP or use a hostname that doesn't change. |
| **Username** | Admin username on your CCU | `Admin` | **Case sensitive!** User must have administrator privileges. |
| **Password** | Password for the admin user | `MySecurePass123` | **Case sensitive!** Only use allowed characters: `A-Z`, `a-z`, `0-9`, and `.!$():;#-` |

### Security & Network Settings

| Setting | Default | When to Use |
|---------|---------|-------------|
| **Use TLS** | `false` | Enable if your CCU uses HTTPS. Changes JSON-RPC port from 80 to 443. **Note:** State updates from CCU to HA are always unencrypted. |
| **Verify TLS** | `false` | Enable to verify TLS certificates. Only enable if your CCU has a valid SSL certificate. |

### Advanced Connection Settings (Optional)

These settings are only needed in special network scenarios:

| Setting | Purpose | When to Use | How to Reset |
|---------|---------|-------------|--------------|
| **Callback Host** | IP/hostname that CCU uses to reach HA | Required if HA runs in Docker with custom networking, or if HA's auto-detected IP is unreachable from the CCU | Set to one blank space character |
| **Callback Port (XML-RPC)** | Port that CCU uses to send state updates | Required in Docker setups where port forwarding is needed | Set to `0` |
| **JSON-RPC Port** | Port for fetching device names and room info | Only if you changed the CCU's JSON-RPC port from default (80/443) | Set to `0` |

#### Docker Users: Network Setup

If running Home Assistant in Docker:
- **Recommended:** Use `network_mode: host` in your Docker configuration
- **Alternative:** If you can't use host networking:
  1. Set **Callback Host** to your Docker host's IP address
  2. Set **Callback Port** to a port you forward to the HA container
  3. Configure port forwarding on your Docker host

---

## Step 2: Interface Selection

Select which device types you want to integrate. Enable only the interfaces your CCU actually uses.

### Common Interface Configurations

#### HomematicIP Only (Most Modern Setups)
```
✓ HomematicIP (HmIP-RF)     Port: 2010 (or 42010 with TLS)
✗ Homematic (BidCos-RF)
✗ Homematic Wired
✗ Heating Groups
✗ CUxD
✗ CCU-Jack
```

#### Mixed Homematic & HomematicIP
```
✓ HomematicIP (HmIP-RF)     Port: 2010 (or 42010 with TLS)
✓ Homematic (BidCos-RF)     Port: 2001 (or 42001 with TLS)
✗ Homematic Wired
✓ Heating Groups            Port: 9292, Path: /groups
✗ CUxD
✗ CCU-Jack
```

### Detailed Interface Options

| Interface | Enable If You Have... | Default Port | TLS Port |
|-----------|----------------------|--------------|----------|
| **HomematicIP (HmIP-RF)** | HomematicIP wireless or wired devices | 2010 | 42010 |
| **Homematic (BidCos-RF)** | Classic Homematic wireless devices | 2001 | 42001 |
| **Homematic Wired (BidCos-Wired)** | Classic Homematic wired devices | 2000 | 42000 |
| **Heating Groups (Virtual Devices)** | Thermostat groups configured in CCU | 9292 | 49292 |
| **CUxD** | CUxD add-on installed | - | - |
| **CCU-Jack** | CCU-Jack software installed | - | - |

**Important Notes:**
- Only enable interfaces you actually use - disabled interfaces save resources
- CUxD and CCU-Jack require additional setup (see [CUxD, CCU-Jack and MQTT support](#cuxd-ccu-jack-and-mqtt-support))
- Port numbers are automatically adjusted when TLS is enabled
- Custom ports can be specified if you changed defaults in your CCU

---

## Step 3: Advanced Options (Optional)

After configuring interfaces, you can choose to configure advanced options or finish setup immediately. Most users can skip this step.

### System Variables & Programs

Control how CCU system variables and programs are imported into Home Assistant.

| Setting | Default | Description | Recommendation |
|---------|---------|-------------|----------------|
| **Enable System Variable Scan** | `true` | Fetch system variables from CCU | Keep enabled unless you don't use system variables |
| **System Variable Markers** | All | Filter which variables to import (HAHM, MQTT, HX, INTERNAL) | Use markers to import only needed variables |
| **Enable Program Scan** | `true` | Fetch programs from CCU | Keep enabled unless you don't use programs |
| **Program Markers** | All except INTERNAL | Filter which programs to import | Use markers to import only needed programs |
| **Scan Interval** | 30 seconds | How often to poll for variable/program changes | Use 30-60s. For values under 15s, use on-demand fetching instead. |

**About Markers:**
Markers are keywords in the description field of system variables/programs in the CCU:
- **HAHM** - Extended mode: Creates writable entities (switch, select, number, text) instead of read-only sensors
- **MQTT** - For CCU-Jack MQTT support: Enables push updates for variables
- **HX** - Custom marker for your own filtering
- **INTERNAL** - CCU's internal checkbox: Includes CCU-internal variables/programs

### Communication & Networking

| Setting | Default | When to Change |
|---------|---------|----------------|
| **System Notifications** | `true` | Shows warnings about CALLBACK and PINGPONG issues. **Don't disable** - fix network issues instead. |
| **Listen on All IPs** | `false` | Enable only for Docker-on-Mac/Windows with double virtualization issues. Security risk if enabled unnecessarily. |

### MQTT Integration (For CUxD and CCU-Jack)

| Setting | Default | Description |
|---------|---------|-------------|
| **Enable MQTT** | `false` | Enable to receive events from CUxD and CCU-Jack devices via MQTT |
| **MQTT Prefix** | _(empty)_ | Set if using MQTT Bridge (RemotePrefix in CCU-Jack config) |

**Prerequisites for MQTT:**
- HA must be connected to an MQTT broker
- CCU-Jack installed OR MQTT Bridge configured
- See [CUxD, CCU-Jack and MQTT support](#cuxd-ccu-jack-and-mqtt-support) for setup guide

### Device Behavior

| Setting | Default | Description | Impact |
|---------|---------|-------------|--------|
| **Enable Sub-Devices** | `false` | Creates separate HA devices for each channel on multi-channel Homematic devices (e.g., HmIP-DRSI4, HmIP-DRDI3) | Affects device-based automations - update automations when changing |
| **Use Group Channel for Cover State** | `true` | Cover groups display level from state channel instead of own level | Only disable if you need to control all three channels separately (experts only) |
| **Delay New Device Creation** | `false` | New devices create a repair notification instead of immediate entity creation | Useful to avoid auto-created names like "VCU1234567:1" - wait until properly named in CCU |

### Expert Options

| Setting | Default | Description |
|---------|---------|-------------|
| **Unignore Parameters** | _(empty)_ | Add normally filtered device parameters as entities | See [Unignore device parameters](#unignore-device-parameters). Use at your own risk. |
| **Optional Settings** | _(empty)_ | Enable debug/analytics features | **Don't use in production** - for development only |

---

## Quick Setup Guide

### Typical HomematicIP Setup (Recommended for Beginners)

**Step 1 - CCU Connection:**
- Instance Name: `ccu3`
- Host: `192.168.1.50`
- Username: `Admin`
- Password: Your CCU admin password
- Use TLS: `false` (unless your CCU requires HTTPS)
- Verify TLS: `false`

**Step 2 - Interfaces:**
- Enable: HomematicIP (HmIP-RF) only
- Use default port: 2010

**Step 3 - Advanced:**
- Click "Complete Setup" to skip advanced options

**Result:** All HomematicIP devices will be discovered and added to Home Assistant.

---

### Advanced Setup with Multiple Device Types

**Step 1 - CCU Connection:**
- Instance Name: `home_ccu` (unique if you have multiple CCUs)
- Host: Your CCU IP/hostname
- Credentials: Admin username and password
- TLS: Enable if your CCU uses HTTPS

**Step 2 - Interfaces:**
- Enable: HomematicIP, Homematic (BidCos-RF), and Heating Groups
- Use default ports (automatically adjusted for TLS)

**Step 3 - Advanced Options:**
- System Variable Markers: Select `HAHM` for writable variables
- Scan Interval: `30` seconds
- Enable MQTT: `true` (if using CUxD or CCU-Jack)
- All other settings: Keep defaults

---

## Reconfiguring the Integration

You can update your CCU connection settings without removing and re-adding the integration:

1. Go to **Settings** → **Devices & Services**
2. Find **Homematic(IP) Local for OpenCCU**
3. Click the **three-dot menu** → **Reconfigure**
4. Update your settings (host, username, password, TLS, etc.)
5. The integration will validate and reload with new settings

**What you can reconfigure:**
- Host/IP address (if CCU moved to different IP)
- Username and password
- TLS settings
- Callback settings
- JSON-RPC port

**Note:** To change interfaces or advanced options, use the **Configure** option instead of Reconfigure.

## System Variables & Programs

System variables and programs from your CCU are automatically imported into Home Assistant as entities. This allows you to read and control CCU logic directly from HA.

### Key Facts

- **Update Frequency:** Polled every 30 seconds (configurable in advanced settings)
- **Initial State:** Created as **disabled** entities - you must enable them manually in HA
- **On-Demand Updates:** Use the `homematicip_local.fetch_system_variables` action for immediate updates
- **Device Location:** All variables/programs appear under a device named after your CCU instance

---

## Understanding System Variables

CCU system variables can be one of five types:

| CCU Type (German) | CCU Type (English) | Default HA Entity | Extended HA Entity (with HAHM) |
|-------------------|-------------------|-------------------|-------------------------------|
| Zeichenkette | Character String | `sensor` (read-only) | `text` (editable) |
| Werteliste | List of Values | `sensor` (read-only) | `select` (editable dropdown) |
| Zahl | Number | `sensor` (read-only) | `number` (editable slider) |
| Logikwert | Logic Value | `binary_sensor` (read-only) | `switch` (togglable) |
| Alarm | Alert | `binary_sensor` (read-only) | `switch` (togglable) |

---

## Two Modes: DEFAULT vs EXTENDED

### DEFAULT Mode (Read-Only)

System variables **without** the `HAHM` marker in their description are created as read-only sensors.

**Example:** A CCU variable named "Temperature_Living_Room" without marker
- ✅ You can read the value in HA
- ❌ You cannot change it from HA's UI (must use action or CCU)

**Created as:**
- Text/List/Number → `sensor.temperature_living_room`
- Logic/Alert → `binary_sensor.temperature_living_room`

---

### EXTENDED Mode (Writable) ⭐ Recommended

System variables **with** the `HAHM` marker in their CCU description become fully controllable in HA.

**How to enable:**
1. In CCU, edit your system variable
2. In the "Description" field, add `HAHM` (uppercase)
3. Save in CCU
4. Reload the integration in HA (or restart HA)

**Example:** A CCU variable "Vacation_Mode" with description "HAHM Holiday switch"
- ✅ You can read the value in HA
- ✅ You can toggle it directly from HA's UI
- ✅ Works with standard HA actions (switch.turn_on, switch.turn_off)
- ✅ Works in device-based automations

**Created as:**
- Text → `text.vacation_mode` (editable text field)
- List → `select.vacation_mode` (dropdown with predefined values)
- Number → `number.vacation_mode` (slider with min/max)
- Logic/Alert → `switch.vacation_mode` (toggle switch)

**Why use EXTENDED mode?**
- Control system variables directly in HA's UI without writing automations
- Use standard HA actions instead of `homematicip_local.set_variable_value`
- Enable/disable device-based automation triggers
- Cleaner integration with HA dashboards

---

## Filtering: Import Only What You Need

By default, the integration imports **all** system variables and programs, which can create hundreds of disabled entities. Use **markers** to filter and auto-enable only the ones you need.

### How Filtering Works

**Without Markers (Default Behavior):**
- All variables/programs imported as **disabled** entities
- You must manually enable each one you want to use
- Disabled entities remain in HA until manually deleted

**With Markers (Recommended):**
- Only marked variables/programs are imported as **enabled** entities
- Unmarked items are not created at all
- When you remove a marker from CCU, HA automatically deletes the entity

### Available Markers

Configure these in **Advanced Options → System Variable Markers / Program Markers**:

| Marker | Where to Add | Purpose | Auto-Enabled? |
|--------|--------------|---------|---------------|
| **HAHM** | Description field | Creates writable entities (select, number, switch, text) | ✅ Yes |
| **MQTT** | Description field | Enables real-time MQTT updates (requires CCU-Jack) | ✅ Yes |
| **HX** | Description field | Generic custom marker for your own filtering | ✅ Yes |
| **INTERNAL** | Checkbox in CCU | Marks CCU-internal variables/programs | ✅ Yes |

### Example: Smart Filtering Setup

**Goal:** Import only vacation mode, heating controls, and alarm status.

**Step 1 - In CCU, edit system variables:**
- "Vacation_Mode" → Description: `HAHM Vacation control`
- "Heating_Setpoint_Living" → Description: `HAHM HX Living room temp`
- "Alarm_Active" → Description: `HAHM Alarm system`
- (All other variables: no marker)

**Step 2 - In HA, configure integration:**
- Advanced Options → System Variable Markers: Select `HAHM` and `HX`

**Result:**
- ✅ Only 3 variables imported (all enabled automatically)
- ✅ All writable (because of HAHM)
- ❌ All other CCU variables ignored

---

## CCU Programs

CCU programs work the same as system variables:

- **Without markers:** All programs (except INTERNAL) imported as disabled `button` entities
- **With markers:** Only marked programs imported as enabled `button` entities
- **Trigger:** Click the button in HA to execute the CCU program

**Tip:** Use the `HAHM` marker on programs you frequently trigger from HA.

---

## Quick Start Guide

### For Beginners (Simple Setup)

**Goal:** Use all system variables without filtering

1. Configure integration (no marker selection needed)
2. All variables appear as disabled entities
3. Go to **Settings → Devices & Services → Entities**
4. Filter by "disabled"
5. Enable the variables you want to use

**Result:** Read-only sensors (use `homematicip_local.set_variable_value` to write)

---

### For Power Users (Filtered + Writable)

**Goal:** Import only needed variables, make them writable

**In CCU:**
1. Edit each important system variable
2. Add `HAHM` to the description field
3. Save

**In HA:**
1. Reconfigure integration → Advanced Options
2. System Variable Markers: Select `HAHM`
3. System Variable Scan: Enabled
4. Save and reload

**Result:**
- Only HAHM-marked variables imported
- All imported variables are writable (switch/select/number/text)
- Auto-enabled (no manual activation needed)

---

## Important Notes

- **Homegear Users:** System variables are always handled in DEFAULT mode (read-only)
- **Changing Modes:** Adding/removing `HAHM` requires HA restart or integration reload to take effect
- **Entity Deletion:** Entities with markers are auto-deleted when marker is removed; unmarked entities must be deleted manually
- **Case Sensitive:** Markers must be uppercase (`HAHM`, not `hahm`)

## Actions

The Homematic(IP) Local for OpenCCU integration makes various custom actions available.

### `homematicip_local.add_link`

Call to `addLink` on the XML-RPC interface.
Creates a direct connection.

### `homematicip_local.clear_cache`

Clears the cache for a central unit from Home Assistant. Requires a restart.

### `homematicip_local.create_central_links`

Creates a central link from a device to the backend. This is required for rf-devices to enable button-press events.
[See](https://github.com/sukramj/homematicip_local?tab=readme-ov-file#events-for-homematicip-devices)

### `homematicip_local.copy_schedule`

__Disclaimer: Too much writing to the device MASTER paramset could kill your device's storage.__

Copies the complete schedule (all profiles P1-P6, all weekdays) from one climate device to another device.

**Requirements:**
- Both devices must support schedules
- Both devices must support the same number of profiles
- Target device will receive an exact copy of the source device's schedule

**Use case:** Quickly replicate a working schedule configuration across multiple identical thermostats.

### `homematicip_local.copy_schedule_profile`

__Disclaimer: Too much writing to the device MASTER paramset could kill your device's storage.__

Copies a single schedule profile from one climate device to another device or to a different profile on the same device.

**Use cases:**
- Copy P1 from Device A to P2 on Device A (create a variant schedule on the same device)
- Copy P1 from Device A to P1 on Device B (replicate to another device)
- Copy P3 from Device A to P1 on Device B (use a different profile slot on target)

**Requirements:**
- Both devices must support schedules
- Cannot copy a profile to itself on the same device (e.g., P1→P1 on same device)
- Target device will receive all weekdays from the source profile

### `homematicip_local.disable_away_mode`

Disable the away mode for `climate` devices. This only works with HomematicIP devices.

### `homematicip_local.enable_away_mode_by_calendar`

Enable the away mode immediately or by start date and time (e.g. 2022-09-01 10:00), and specify the end by date and time (e.g. 2022-10-01 10:00). This only works with HomematicIP devices.

### `homematicip_local.enable_away_mode_by_duration`

Enable the away mode immediately, and specify the end time by setting a duration (in hours). This only works with HomematicIP devices.

### `homematicip_local.export_device_definition`

Exports a device definition (2 files) to

- 'Your home-assistant config directory'/homematicip_local/export_device_descriptions/{device_type}.json
- 'Your home-assistant config directory'/homematicip_local/export_paramset_descriptions/{device_type}.json

Please create a pull request with both files at [pydevccu](https://github.com/sukramj/pydevccu), if the device not exists, to support future development of this component.
This data can be used by the developers to add customized entities for new devices.

### `homematicip_local.fetch_system_variables`

action to fetch system variables on demand from backend independent from default 30s schedule.
Using this action too often could have a negative effect on the stability of your backend.

### `homematicip_local.force_device_availability`

Reactivate a device in Home Assistant that has been made unavailable by an UNREACH event from CCU.
This action will only override the availability status of a device and all its dependent entities. There is no communication to the backend to enforce a reactivation!

This is not a solution for communication problems with Homematic devices.
Use this only to reactivate devices with flaky communication to gain control again.

### `homematicip_local.get_device_value`

Get a device parameter via the XML-RPC interface.

### `homematicip_local.get_link_peers`

Call to `getLinkPeers` on the XML-RPC interface.
Returns a dict of direct connection partners

### `homematicip_local.get_paramset`

Call to `getParamset` on the XML-RPC interface.
Returns a paramset

### `homematicip_local.get_link_paramset`

Call to `getParamset` for direct connections on the XML-RPC interface.
Returns a paramset

### `homematicip_local.get_schedule_profile`

Returns the schedule of a climate profile (e.g., P1, P2, etc.).

**Return format:** The returned data contains all weekdays for the specified profile. Redundant 24:00 slots are automatically filtered out, so you typically receive only the meaningful time slots (usually 3-7 slots instead of 13).

**Example structure:**
```yaml
MONDAY:
  1:
    ENDTIME: "06:00"
    TEMPERATURE: 18.0
  2:
    ENDTIME: "22:00"
    TEMPERATURE: 21.0
  3:
    ENDTIME: "24:00"
    TEMPERATURE: 18.0
TUESDAY:
  ...
```

### `homematicip_local.get_schedule_weekday`

Returns the schedule of a climate profile for a specific weekday.

**Return format:** The returned data is filtered to show only meaningful slots. Redundant 24:00 slots at the end are removed automatically. Each slot defines a temperature period that ends at the specified ENDTIME.

**Example structure:**
```yaml
1:
  ENDTIME: "06:00"
  TEMPERATURE: 18.0
2:
  ENDTIME: "08:00"
  TEMPERATURE: 21.0
3:
  ENDTIME: "24:00"
  TEMPERATURE: 18.0
```

**Understanding slots:**
- Slot 1 means: From 00:00 until 06:00, maintain 18.0°C
- Slot 2 means: From 06:00 until 08:00, maintain 21.0°C
- Slot 3 means: From 08:00 until 24:00, maintain 18.0°C

### `homematicip_local.put_paramset`

__Disclaimer: Too much writing to the device MASTER paramset could kill your device's storage.__

Call to `putParamset` on the XML-RPC interface.

### `homematicip_local.put_link_paramset`

__Disclaimer: Too much writing to the device MASTER paramset could kill your device's storage.__

Call to `putParamset` for direct connections on the XML-RPC interface.

### `homematicip_local.record_session`

Records a session for a central unit for a given time. The output is stored in 'Your home-assistant config directory'/homematicip_local/session/
This is useful for debugging. The output contains a maximum of 10 minutes of data.

### `homematicip_local.remove_central_links`

Removes a central link from the backend. This is required to disable enable button-press events.

### `homematicip_local.remove_link`

Call to `removeLink` on the XML-RPC interface.
Removes a direct connection.

### `homematicip_local.set_cover_combined_position`

Move a blind to a specific position and tilt position.

### `homematicip_local.set_device_value`

__Disclaimer: Too much writing to the device MASTER paramset could kill your device's storage.__

Set a device parameter via the XML-RPC interface. Preferred when using the UI. Works with device selection.

### `homematicip_local.set_schedule_profile`

__Disclaimer: Too much writing to the device could kill your device's storage.__

Sends a complete schedule for a climate profile (all weekdays) to a device.

**Input data format:** The data structure matches what you get from `get_schedule_profile`. You can provide partial data (fewer than 13 slots per weekday), and the system will automatically:
- Sort slots chronologically by ENDTIME
- Fill missing slots up to 13 with 24:00 entries
- Validate temperature ranges and time sequences

**Requirements:**
- Temperature values must be within the device's supported range (typically 4.5°C - 30.5°C)
- ENDTIME values must use "HH:MM" format (e.g., "06:00", "24:00")
- Each slot's ENDTIME must be equal to or later than the previous slot

**Important:** The required data structure can be retrieved with `get_schedule_profile`, modified as needed, and sent back.

### `homematicip_local.set_schedule_weekday`

__Disclaimer: Too much writing to the device could kill your device's storage.__

Sends the schedule for a single weekday of a climate profile to a device.
See the [sample](#sample-for-set_schedule_weekday) below.

**Remarks:**
- Not all devices support schedules. This is currently only supported by this integration for HmIP devices.
- Not all devices support six profiles (P1-P6).
- There is currently no matching UI component in Home Assistant.

**Input data format:** You can provide the schedule in two ways:

1. **Partial format** (recommended): Provide only the meaningful slots. The system will automatically fill missing slots to reach exactly 13 slots.
   ```yaml
   weekday_data:
     1:
       ENDTIME: "06:00"
       TEMPERATURE: 18
     2:
       ENDTIME: "22:00"
       TEMPERATURE: 21
     3:
       ENDTIME: "24:00"
       TEMPERATURE: 18
   ```

2. **Full format**: Provide all 13 slots explicitly (as shown in the [sample](#sample-for-set_schedule_weekday) below).

**Automatic processing:**
- String keys are converted to integers (both `"1"` and `1` work)
- Slots are sorted chronologically by ENDTIME
- Missing slots are filled with 24:00 entries using the last slot's temperature
- Data is validated for temperature ranges and time sequences

**Requirements:**
- Temperature must be in the device's defined range (typically 4.5°C - 30.5°C)
- ENDTIME format must be "HH:MM" (e.g., "06:00", "24:00")
- Each ENDTIME must be equal to or later than the previous slot's ENDTIME

**Note:** When you retrieve a schedule with `get_schedule_weekday`, you receive filtered data (fewer slots). You can use this data directly with `set_schedule_weekday` - the system will automatically normalize it to 13 slots.

### `homematicip_local.set_schedule_simple_profile`

__Disclaimer: Too much writing to the device could kill your device's storage.__

Sends a complete schedule for a climate profile to a device using a **simplified format**.

**Why use this?** The simple format is easier to write and understand - you only specify the temperature periods you care about, without worrying about 13 slots or filling gaps.

**How it works:**
- You specify only the active heating/cooling periods with STARTTIME, ENDTIME, and TEMPERATURE
- The system automatically fills gaps with `base_temperature`
- All time periods outside your specified slots use `base_temperature`
- The system converts everything to the required 13-slot format automatically

**Example:** See [sample](#sample-for-set_schedule_simple_profile) below for the full data structure.

### `homematicip_local.set_schedule_simple_weekday`

__Disclaimer: Too much writing to the device could kill your device's storage.__

Sends the schedule for a single weekday of a climate profile using a **simplified format**.

**Why use this?** Instead of managing 13 slots, you only define the specific temperature periods you need.

**How it works:**
1. You provide a list of temperature periods with STARTTIME, ENDTIME, and TEMPERATURE
2. You specify a `base_temperature` for all times not covered by your periods
3. The system automatically:
   - Sorts your periods chronologically
   - Fills gaps between periods with `base_temperature`
   - Converts to the required 13-slot format
   - Validates all ranges and sequences

**Example:**
```yaml
base_temperature: 18.0
simple_weekday_list:
  - STARTTIME: "06:00"
    ENDTIME: "08:00"
    TEMPERATURE: 21.0
  - STARTTIME: "17:00"
    ENDTIME: "22:00"
    TEMPERATURE: 21.0
```

This creates:
- 00:00-06:00: 18.0°C (base_temperature)
- 06:00-08:00: 21.0°C (your first period)
- 08:00-17:00: 18.0°C (base_temperature fills gap)
- 17:00-22:00: 21.0°C (your second period)
- 22:00-24:00: 18.0°C (base_temperature)

See the [sample](#sample-for-set_schedule_weekday) below for a complete example. 

### `homematicip_local.get_variable_value`

Get the value variable from your Homematic hub.

### `homematicip_local.set_variable_value`

Set the value of a variable on your Homematic hub.

Value lists accept the 0-based list position or the value as input.

For booleans the following values can be used:

- 'true', 'on', '1', 1 -> True
- 'false', 'off', '0', 0 -> False

### `homematicip_local.turn_on_siren`

Turn siren on. Siren can be disabled by siren.turn_off. Useful helpers for siren can be found [here](https://github.com/sukramj/aiohomematic/blob/devel/docs/input_select_helper.md#siren).

### `homematicip_local.light_set_on_time`

Set on time for a light entity. Must be followed by a `light.turn_on`.
Use 0 to reset the on time.

### `homematicip_local.switch_set_on_time`

Set on time for a switch entity. Must be followed by a `switch.turn_on`.
Use 0 to reset the on time.

### `homeassistant.update_entity`

Update the value of an entity (only required for edge cases). An entity can be updated at most every 60 seconds.

This action is not needed to update entities in general, because 99,9% of the entities and values are getting updated by this integration automatically. But with this action, you can manually update the value of an entity - **if you really need this in special cases**, e.g. if the value is not updated or not available, because of design gaps or bugs in the backend or device firmware (e.g. rssi-values of some HM-devices).

Attention: This action gets the value for the entity via a 'getValue' from the backend, so the values are updated afterwards from the backend cache (for battery devices) or directly from the device (for non-battery devices). So even with using this action, the values are still not guaranteed for the battery devices and there is a negative impact on the duty cycle of the backend for non-battery devices.

### `homeassistant.update_device_firmware_data`

Update the firmware data for all devices. For more information see [updating the firmware](https://github.com/sukramj/homematicip_local#updating-the-firmware)

## Events

Events fired by this integration that can be consumed by users.

### `homematic.keypress`

This event type is used when a key is pressed on a device,
and can be used with device triggers or event entities in automation, so manual event listening is not necessary.

In this context, the following must also be observed: [Events for Homematic(IP) devices](https://github.com/sukramj/homematicip_local#events-for-homematicip-devices)

The `PRESS*` parameters are evaluated for this event type in the backend.

### `homematic.device_availability`

This event type is used when a device is no longer available or is available again,
and can be used with the blueprint [Support for persistent notifications for unavailable devices](https://github.com/sukramj/homematicip_local/blob/devel/blueprints/automation/homematicip_local_persistent_notification.yaml).

The `UNREACH` parameter is evaluated for this event type in the backend.

### `homematic.device_error`

This event type is used when a device is in an error state.
A sample usage is shown in the blueprint [Show device errors](https://github.com/sukramj/homematicip_local/blob/devel/blueprints/automation/homematicip_local_show_device_error.yaml).

The `ERROR*` parameters are evaluated for this event type in the backend.

## Additional Information

This section covers common questions, best practices, and important concepts for working with the integration.

---

## Understanding Entity States & Updates

### How State Updates Work

The integration uses a **push-based** system, not polling:

1. **Initial Load:** When HA starts or reconnects, all device states are fetched from CCU
2. **Ongoing Updates:** CCU sends state changes to HA via XML-RPC events (push)
3. **Exception:** System variables are polled every 30 seconds (configurable)

**Important:** After a CCU restart, the CCU itself doesn't know device states until devices report in. Battery devices may take hours to update.

### The `value_state` Attribute

Every entity has a `value_state` attribute indicating how reliable the current value is:

| State | Meaning | When It Occurs | Trust Level |
|-------|---------|----------------|-------------|
| **`valid`** | Value loaded from CCU or received via event | Normal operation | ✅ Fully reliable |
| **`not valid`** | No value available | Device never reported | ❌ Unknown state |
| **`restored`** | Value restored from last HA session | After HA restart | ⚠️ May be outdated |
| **`uncertain`** | CCU restarted, no update received yet | After CCU restart | ⚠️ Possibly outdated |

**Recommendation:** For critical automations, check `value_state == "valid"` to ensure current data.

### Optimized Backend Calls

The integration minimizes unnecessary CCU communication:

- **Single-parameter entities** (switch, sensor): Only sends changes if value differs
- **Multi-parameter entities** (climate, cover, light): Sends if any parameter changed
- **Not optimized:** Locks, sirens, system variables, and certain actions always send commands

---

## Managing Devices & Entities

### Removing Devices

**To remove a device from Home Assistant:**

1. Go to **Settings** → **Devices & Services** → **Homematic(IP) Local**
2. Click on the device
3. Click the **three-dot menu** → **Delete**

**Important:** This only removes the device from HA, not from your CCU.

### Renaming Devices After CCU Changes

If you renamed a device/channel in the CCU and want the change reflected in HA:

| Method | Steps | Entity ID | Name | When to Use |
|--------|-------|-----------|------|-------------|
| **1. Manual rename in HA** | Rename in HA entity settings | Unchanged | Changed | Quick fix, but not synced with CCU |
| **2. Reload integration** | Settings → Integrations → Reload | Unchanged | Updated from CCU | Keep entity_id, update name |
| **3. Delete & recreate** | Delete device in HA → Reload integration | New (based on new name) | Updated from CCU | Want entity_id to match new name |
| **4. Reinstall integration** | Remove & re-add integration | All new | All updated | Fresh start (lose customizations) |

**Recommendation:** Use method 2 for most cases.

### CCU Rooms → HA Areas

**How room assignments work:**

| CCU Room Configuration | HA Area Assignment | Example |
|----------------------|-------------------|---------|
| Single room assigned to all channels | ✅ Assigned | Device in "Living Room" → Area: "Living Room" |
| Same room assigned to multiple channels | ✅ Assigned | All channels in "Kitchen" → Area: "Kitchen" |
| Different rooms per channel | ❌ Not assigned | Ch1: "Kitchen", Ch2: "Bedroom" → Area: (none) |
| No rooms assigned | ❌ Not assigned | No CCU rooms → Area: (none) |

**Limitation:** HA allows one area per device; CCU allows multiple rooms per channel.

---

## Working with Device Parameters

### Deactivated vs Disabled Entities

**Many entities are created but initially disabled** to avoid cluttering your HA instance. To use them:

1. Go to **Settings** → **Devices & Services** → **Entities**
2. Filter by "Disabled"
3. Click the entity → **Enable**

**Common disabled entities:**
- RSSI (signal strength) sensors
- Advanced diagnostic parameters
- Rarely used device features

### Unignoring Parameters

Some parameters are completely filtered out (not created at all). To add them:

1. **Check first:** The parameter might exist as a disabled entity (see above)
2. **If truly missing:** Configure in **Advanced Options** → **Unignore Parameters**
3. See [detailed documentation](https://github.com/sukramj/aiohomematic/blob/devel/docs/unignore.md)

**⚠️ Warning:** Use at your own risk - these parameters are filtered for good reasons.

### Special Case: HmIP-eTRV LEVEL Parameter

The thermostat valve `LEVEL` parameter is intentionally created as a **sensor** (read-only), not a **number** entity:

**Why?** The valve's internal control immediately overrides any manual position change, making manual control useless.

**If you still need it:** Use the unignore feature to add `LEVEL` as a number entity.

---

## Button Devices & Events

### Why Buttons Don't Show Entities

Devices with physical buttons (remotes, motion detectors with buttons) don't create button entities because:
- Buttons don't have persistent state (pressed vs not pressed)
- Events are the proper way to handle button presses in HA

**Example:** HM-Sen-MDIR-WM55 motion detector
- ✅ Shows: Motion sensor, brightness sensor
- ❌ Doesn't show: Two internal buttons

### Using Buttons in Automations

**Correct approach:**
1. Create an automation
2. Trigger type: **Device**
3. Select your button device
4. Select specific trigger: "Button 1 pressed", "Button 2 long pressed", etc.

**Alternative:** Use the `homematic.keypress` event (advanced users)

### Enabling Button Events

For HomematicIP devices (WRC2, WRC6, SPDR, KRC4, HM-PBI-4-FM), button events require activation:

**Option A - Easiest (Action):**
```yaml
action: homematicip_local.create_central_links
target:
  device_id: YOUR_DEVICE_ID
```

**Option B - OpenCCU Users:**
1. Go to CCU → Settings → Devices
2. Click "+" next to your remote control
3. Click the button channel
4. Press "activate"

**Option C - CCU Program (Classic Method):**
1. CCU → Programs and connections → New program
2. Add condition: Device selection → Select button channel
3. Choose press type (short/long)
4. Save program (can be set inactive after first trigger)

**To disable events:** Use `homematicip_local.remove_central_links`

### Triggering CCU Buttons from HA

**Use case:** Press a virtual CCU button to trigger a CCU program

```yaml
action: homematicip_local.set_device_value
data:
  device_id: abcdefg...
  parameter: PRESS_SHORT
  value: "true"
  value_type: boolean
  channel: 3
```

---

## Troubleshooting Common Issues

### "Error fetching initial data"

**What it means:** The integration couldn't process the CCU's initial data response.

**Why it happens:** The CCU's REGA script returned invalid data (rare).

**Impact:** Integration falls back to individual requests (slower startup, higher CCU load).

**This is NOT a bug in the integration.** It's a CCU data issue.

**How to diagnose:**
1. Get the [REGA script](https://github.com/sukramj/aiohomematic/blob/devel/aiohomematic/rega_scripts/fetch_all_device_data.fn)
2. Replace `##interface##` (line 17) with the interface from the error message
3. Run in CCU web interface
4. Check if output is valid JSON
5. Search discussions for "GET_ALL_DEVICE_DATA"

**What to do:** Post in [Discussions](https://github.com/sukramj/aiohomematic/discussions) with script output.

---

### "XmlRPC-Server received no events"

**What it means:** HA isn't receiving state updates from CCU for 10+ minutes.

**How the check works:**
- HA sends PING to CCU every 15 seconds
- Expects PONG response via XML-RPC server
- Alert triggers after 10 minutes of missing PONGs/updates

**This is a network communication problem, not an integration bug.**

**Common causes:**
1. Firewall blocking CCU → HA connection
2. Docker networking issues (callback_host not configured)
3. CCU overloaded or unresponsive
4. Network issues between CCU and HA

**How to fix:**
1. Check firewall rules (allow CCU → HA on callback port)
2. Docker users: Set `callback_host` and `callback_port_xml_rpc`
3. Verify CCU is responsive
4. Check HA logs for connection errors

---

### "Pending Pong mismatch"

**What it means:** Number of sent PINGs doesn't match received PONGs.

**Scenario 1: Fewer PONGs received**
- **Cause:** Another HA instance with same `instance_name` started after this one
- **Effect:** That instance receives all events (including device updates)
- **Alternative cause:** CCU or network communication problem

**Scenario 2: More PONGs received**
- **Cause:** Another HA instance with same `instance_name` started before this one
- **Effect:** This instance receives events from both

**Solution:** Ensure each HA instance has a unique `instance_name` when connecting to the same CCU.

---

## Technical Details

### RSSI Signal Strength

See [detailed explanation](https://github.com/sukramj/aiohomematic/blob/devel/docs/rssi_fix.md) of how RSSI values are calculated and fixed.

## Updating Device Firmware

This integration provides **update entities** for each device, allowing you to manage firmware updates from Home Assistant.

### How Firmware Updates Work

**The Process:**

1. **Upload firmware** to CCU (via CCU web interface)
2. **CCU transfers firmware** to device (can take hours or days)
3. **Install firmware** via HA update entity

**Important:** Firmware files come from your CCU, not from eQ-3 servers. Upload firmware to CCU first.

### Update Check Schedule

The integration polls CCU for firmware information on these schedules:

| Scenario | Check Frequency | Reason |
|----------|----------------|---------|
| **Normal operation** | Every 6 hours | Firmware updates are rare |
| **Transfer in progress** | Every hour | Monitor active transfers |
| **Installation in progress** | Every 5 minutes | Quick feedback during install |

### Using Firmware Updates in HA

**Step 1: Upload firmware to CCU**
- Use CCU web interface → Settings → System Control → Firmware Update
- Upload .eq3 firmware file

**Step 2: Wait for transfer**
- CCU transfers firmware to device (background process)
- Can take hours or days depending on device type

**Step 3: Install from HA**
1. Go to **Settings** → **Devices & Services**
2. Find your device
3. Click the **Update** entity
4. Click **Install**

**Status meanings:**
- **Update available:** Firmware transferred, ready to install
- **Installing:** Update command sent to device
- **In process:** Waiting for device to accept command
- **Up to date:** Device running latest firmware

### Update Latency

- **Firmware availability status:** Can be delayed up to **1 hour** in HA
- **Installation status:** Updates every **5 minutes** during install

### On-Demand Update Check

Force immediate firmware status check:

```yaml
action: homeassistant.update_device_firmware_data
```

**⚠️ Warning:** Frequent manual checks may impact CCU performance!

## CUxD, CCU-Jack & MQTT Support

CUxD and CCU-Jack devices require special integration because they don't use the standard XML-RPC protocol.

### Communication Methods

| Device Type | Default Method | MQTT Method (Optional) |
|-------------|---------------|----------------------|
| **CUxD** | JSON-RPC polling (every 15s) | MQTT push events (no polling) |
| **CCU-Jack** | JSON-RPC polling (every 15s) | MQTT push events (no polling) |
| **System Variables (with MQTT marker)** | Polling (every 30s) | MQTT push events (instant) |

**Why MQTT is better:** Real-time updates instead of polling, less CCU load.

---

## Setting Up MQTT Support

MQTT enables instant push updates for CUxD, CCU-Jack devices, and marked system variables.

### Prerequisites

✅ **Required:**
1. CCU-Jack installed on your CCU
2. HA connected to an MQTT broker
3. MQTT integration configured in HA

📚 **Documentation:**
- [HA MQTT Integration Guide](https://www.home-assistant.io/integrations/mqtt/)
- [CCU-Jack Documentation](https://github.com/mdzio/ccu-jack/wiki)
- [CCU-Jack MQTT Bridge](https://github.com/mdzio/ccu-jack/wiki/MQTT-Bridge)

### Setup Option 1: Direct Connection (Recommended)

**Use CCU-Jack's built-in MQTT broker:**

1. **Configure CCU-Jack** to enable MQTT broker
2. **Connect HA** to CCU-Jack's MQTT broker
3. **Enable MQTT in integration:**
   - Advanced Options → Enable MQTT: `true`
   - MQTT Prefix: _(leave empty)_

### Setup Option 2: MQTT Bridge

**Use external MQTT broker with CCU-Jack bridge:**

1. **Configure CCU-Jack** to use MQTT Bridge with RemotePrefix
2. **Connect HA** to your external MQTT broker
3. **Enable MQTT in integration:**
   - Advanced Options → Enable MQTT: `true`
   - MQTT Prefix: `<your RemotePrefix from CCU-Jack>`

### Enabling System Variable MQTT Updates

To get instant updates for CCU system variables via MQTT:

1. **In CCU:** Edit system variable
2. **Add marker** to description: `MQTT`
3. **In HA:** Enable MQTT in integration advanced options

**Example:** Variable "Heating_Mode" with description `MQTT HAHM Temperature control`
- ✅ Receives instant MQTT updates
- ✅ Writable (because of HAHM marker)

### Troubleshooting MQTT

**Before opening an issue:**
1. Use an MQTT explorer tool (MQTT Explorer, mosquitto_sub)
2. Verify CCU-Jack is publishing messages
3. Check topics match expected format
4. Confirm HA's MQTT integration receives messages

---

## CUxD & CCU-Jack Device Compatibility

**How it works:**
- CUxD and CCU-Jack emulate Homematic device descriptions
- Integration treats them like standard Homematic devices
- Behavior may differ from original hardware

**Important Limitations:**
- This integration targets **original Homematic hardware** behavior
- CUxD/CCU-Jack differences are **not considered bugs**
- Use HA templates/customizations to adapt behavior if needed

**Support Policy:**
- ✅ Supported: Standard device emulation
- ❌ Not supported: CUxD/CCU-Jack specific features or quirks

If CUxD or CCU-Jack behaves differently than expected, adapt using HA's templating features rather than requesting integration changes.

## Troubleshooting

If the integration does not work as expected, try the following before opening an issue:
- Review Home Assistant logs for entries related to this integration: homematicip_local and aiohomematic. Address any errors or warnings shown.
- Verify required ports are open and reachable between HA and your hub (CCU/OpenCCU/Homegear). See Firewall and required ports above.
- Ensure the CCU user has admin privileges and that your password only contains supported characters (A-Z, a-z, 0-9 and .!$():;#-).
- When running HA in Docker, prefer network_mode: host. Otherwise, set callback_host and callback_port_xml_rpc in the configuration and allow inbound connections from the CCU to that port.
- If you run multiple HA instances or connect to multiple CCUs, make instance_name unique per HA instance.
- For persistent auto-discovery entries after setup, click Ignore or reconfigure the existing instance, then restart HA.
- After updating CCU firmware or changing interfaces, restart Home Assistant and reload the integration.
- For CUxD/CCU-Jack, ensure MQTT is set up correctly and verify topics/events with an MQTT Explorer before reporting issues.

## Frequently asked questions

Q: I can see an entity, but it is unavailable.<br>
A: Possible reason: the entity is deactivated. Go into the entity configuration and activate the entity.

Q: I'm using a button on a remote control as a trigger in an automation, but the automation doesn't fire after the button is pressed.<br>
A: See [Events for Homematic(IP) devices](#events-for-homematicip-devices)

Q: My device is not listed under [Events for Homematic(IP) devices](#events-for-homematicip-devices)<br>
A: It doesn't matter. These are just examples. If you can press it, it is a button and events are emitted.

Q: I have a problem with the integration. What can I do?<br>
A: Before creating an issue, you should review the HA log files for `error` or `warning` entries related to this integration (`homematicip_local`, `aiohomematic`) and read the corresponding messages. You can find further information about some messages in this document.

Q: What is the source of OPERATING_VOLTAGE_LEVEL, APPARENT_TEMPERATURE, DEW_POINT, FROST_POINT, VAPOR_CONCENTRATION
A: These are parameters/sensors, that are [calculated](https://github.com/SukramJ/aiohomematic/blob/devel/docs/calculated_climate_sensors.md) based on existing parameters to add more information to a device.

## Examples in YAML


### Sample for set_variable_value
Set a boolean variable to true:

```yaml
---
action: homematicip_local.set_variable_value
data:
  entity_id: sensor.ccu2
  name: Variable name
  value: true
```

### Sample for set_device_value
Manually turn on a switch actor:

```yaml
---
action: homematicip_local.set_device_value
data:
  device_id: abcdefg...
  channel: 1
  parameter: STATE
  value: "true"
  value_type: boolean
```

### Sample 2 for set_device_value
Manually set temperature on thermostat:

```yaml
---
action: homematicip_local.set_device_value
data:
  device_id: abcdefg...
  channel: 4
  parameter: SET_TEMPERATURE
  value: "23.0"
  value_type: double
```

### Sample for set_schedule_weekday

Send a climate schedule for Monday using the **full 13-slot format**:

```yaml
---
action: homematicip_local.set_schedule_weekday
target:
  entity_id: climate.heizkorperthermostat_db
data:
  profile: P3
  weekday: MONDAY
  weekday_data:
    # You can use either string keys ("1") or integer keys (1)
    "1":
      ENDTIME: "05:00"
      TEMPERATURE: 16
    "2":
      ENDTIME: "06:00"
      TEMPERATURE: 17
    "3":
      ENDTIME: "09:00"
      TEMPERATURE: 16
    "4":
      ENDTIME: "15:00"
      TEMPERATURE: 17
    "5":
      ENDTIME: "19:00"
      TEMPERATURE: 16
    "6":
      ENDTIME: "22:00"
      TEMPERATURE: 22
    "7":
      ENDTIME: "24:00"
      TEMPERATURE: 16
    # Slots 8-13 are filled with 24:00 (unused slots)
    "8":
      ENDTIME: "24:00"
      TEMPERATURE: 16
    "9":
      ENDTIME: "24:00"
      TEMPERATURE: 16
    "10":
      ENDTIME: "24:00"
      TEMPERATURE: 16
    "11":
      ENDTIME: "24:00"
      TEMPERATURE: 16
    "12":
      ENDTIME: "24:00"
      TEMPERATURE: 16
    "13":
      ENDTIME: "24:00"
      TEMPERATURE: 16
```

**Alternative: Partial format** (recommended, easier to write):
```yaml
---
action: homematicip_local.set_schedule_weekday
target:
  entity_id: climate.heizkorperthermostat_db
data:
  profile: P3
  weekday: MONDAY
  weekday_data:
    # Only specify meaningful slots - system fills the rest automatically
    1:
      ENDTIME: "05:00"
      TEMPERATURE: 16
    2:
      ENDTIME: "06:00"
      TEMPERATURE: 17
    3:
      ENDTIME: "09:00"
      TEMPERATURE: 16
    4:
      ENDTIME: "15:00"
      TEMPERATURE: 17
    5:
      ENDTIME: "19:00"
      TEMPERATURE: 16
    6:
      ENDTIME: "22:00"
      TEMPERATURE: 22
    7:
      ENDTIME: "24:00"
      TEMPERATURE: 16
    # Slots 8-13 are automatically filled with ENDTIME: "24:00" and TEMPERATURE: 16
```

### Sample for set_schedule_simple_profile

Send a simple climate profile (all weekdays) to the device:

**What this does:** Sets profile P1 with a base temperature of 4.5°C. For each weekday, three heating periods are defined. All other times use the base temperature.

```yaml
---
action: homematicip_local.set_schedule_simple_profile
target:
  entity_id: climate.heizkorperthermostat_db
data:
  base_temperature: 4.5  # Temperature for all times not covered by periods below
  profile: P1
  simple_profile_data:
    MONDAY:
      # Morning warm-up: 05:00-06:00 at 17°C
      - TEMPERATURE: 17
        STARTTIME: "05:00"
        ENDTIME: "06:00"
      # Daytime: 09:00-15:00 at 17°C
      - TEMPERATURE: 17
        STARTTIME: "09:00"
        ENDTIME: "15:00"
      # Evening: 19:00-22:00 at 22°C
      - TEMPERATURE: 22
        STARTTIME: "19:00"
        ENDTIME: "22:00"
      # All other times (00:00-05:00, 06:00-09:00, 15:00-19:00, 22:00-24:00) use base_temperature 4.5°C
    TUESDAY:
      - TEMPERATURE: 17
        STARTTIME: "05:00"
        ENDTIME: "06:00"
      - TEMPERATURE: 17
        STARTTIME: "09:00"
        ENDTIME: "15:00"
      - TEMPERATURE: 22
        STARTTIME: "19:00"
        ENDTIME: "22:00"
    # Add other weekdays as needed (WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY)
```

### Sample for set_schedule_simple_weekday

Send a simple climate schedule for Monday only:

**What this does:** Sets Monday's schedule for profile P3. Three heating periods are defined. The base temperature (16°C) is used for all other times.

```yaml
---
action: homematicip_local.set_schedule_simple_weekday
target:
  entity_id: climate.heizkorperthermostat_db
data:
  profile: P3
  weekday: MONDAY
  base_temperature: 16  # Temperature for all times not covered by periods below
  simple_weekday_list:
    # Morning warm-up: 05:00-06:00 at 17°C
    - TEMPERATURE: 17
      STARTTIME: "05:00"
      ENDTIME: "06:00"
    # Daytime: 09:00-15:00 at 17°C
    - TEMPERATURE: 17
      STARTTIME: "09:00"
      ENDTIME: "15:00"
    # Evening: 19:00-22:00 at 22°C
    - TEMPERATURE: 22
      STARTTIME: "19:00"
      ENDTIME: "22:00"
    # All other times (00:00-05:00, 06:00-09:00, 15:00-19:00, 22:00-24:00) use base_temperature 16°C
```

**Result:** The system converts this to 13 slots:
- Slot 1-5: Times from 00:00 to 05:00, 06:00 to 09:00, 15:00 to 19:00, and 22:00 to 24:00 use 16°C
- Slots for your defined periods use 17°C and 22°C
- All slots sorted chronologically and filled to exactly 13 slots

### Sample for put_paramset
Set the week program of a wall thermostat:

```yaml
---
action: homematicip_local.put_paramset
data:
  device_id: abcdefg...
  paramset_key: MASTER
  paramset:
    WEEK_PROGRAM_POINTER: 1
```

### Sample 2 for put_paramset
Set the week program of a wall thermostat with explicit `rx_mode` (BidCos-RF only):

```yaml
---
action: homematicip_local.put_paramset
data:
  device_id: abcdefg...
  paramset_key: MASTER
  rx_mode: WAKEUP
  paramset:
    WEEK_PROGRAM_POINTER: 1
```

BidCos-RF devices have an optional parameter for put_paramset which defines the way the configuration data is sent to the device.

`rx_mode` `BURST`, which is the default value, will wake up every device when submitting the configuration data and hence makes all devices use some battery. It is instant, i.e. the data is sent almost immediately.

`rx_mode` `WAKEUP` will send the configuration data only after a device submitted updated values to CCU, which usually happens every 3 minutes. It will not wake up every device and thus saves devices battery.

## Available Blueprints

The following blueprints can be used to simplify the usage of Homematic and HomematicIP device:

- [Support for 2-button Remotes](https://github.com/sukramj/homematicip_local/blob/devel/blueprints/automation/homematicip_local-actions-for-2-button.yaml): Support for two button remote like HmIP-WRC2.
- [Support for 4-button Key Ring Remote Control](https://github.com/sukramj/homematicip_local/blob/devel/blueprints/automation/homematicip_local-actions-for-key_ring_remote_control.yaml): Support for four button remote like HmIP-KRCA.
- [Support for 6-button Remotes](https://github.com/sukramj/homematicip_local/blob/devel/blueprints/automation/homematicip_local-actions-for-6-button.yaml): Support for six button remote like HmIP-WRC6.
- [Support for 8-button Remotes](https://github.com/sukramj/homematicip_local/blob/devel/blueprints/automation/homematicip_local-actions-for-8-button.yaml): Support for eight button remote like HmIP-RC8.
- [Support for persistent notifications for unavailable devices](https://github.com/sukramj/homematicip_local/blob/devel/blueprints/automation/homematicip_local_persistent_notification.yaml): Enable persistent notifications about unavailable devices.
- [Reactivate device by model](https://github.com/sukramj/homematicip_local/blob/devel/blueprints/automation/homematicip_local_reactivate_device_by_model.yaml). Reactivate unavailable devices by device model.
- [Reactivate every device](https://github.com/sukramj/homematicip_local/blob/devel/blueprints/automation/homematicip_local_reactivate_device_full.yaml). Reactivate all unavailable devices. NOT recommended. Usage of `by device type` or `single device` should be preferred.
- [Reactivate single device](https://github.com/sukramj/homematicip_local/blob/devel/blueprints/automation/homematicip_local_reactivate_single_device.yaml) Reactivate a single unavailable device.
- [Show device errors](https://github.com/sukramj/homematicip_local/blob/devel/blueprints/automation/homematicip_local_show_device_error.yaml) Show all error events emitted by a device. This is an unfiltered blueprint. More filters should be added to the trigger.

Feel free to contribute:

- [Community blueprints](https://github.com/sukramj/homematicip_local/blob/devel/blueprints/community)

I use these blueprints on my own system and share them with you, but I don't want to invest in blueprints for devices that I don't own!
Feel free to copy, improve, or enhance these blueprints and adapt them to other devices, and if you like, create a PR with a new blueprint.

Just copy these files to "your ha-config_dir"/blueprints/automation


## Support and Contributing

- Issues: https://github.com/sukramj/aiohomematic/issues
- Discussions: https://github.com/sukramj/aiohomematic/discussions
- Wiki contributions are welcome: https://github.com/sukramj/aiohomematic/wiki
- Pull requests are welcome in this repository. Please open an issue or discussion first if you plan larger changes.


[license-shield]: https://img.shields.io/github/license/SukramJ/homematicip_local.svg?style=for-the-badge
[release]: https://github.com/SukramJ/homematicip_local/releases
[releasebadge]: https://img.shields.io/github/v/release/SukramJ/homematicip_local?style=for-the-badge
[hainstall]: https://my.home-assistant.io/redirect/config_flow_start/?domain=homematicip_local
[hainstallbadge]: https://img.shields.io/badge/dynamic/json?style=for-the-badge&logo=home-assistant&logoColor=ccc&label=usage&suffix=%20installs&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.homematicip_local.total
[sponsorsbadge]: https://img.shields.io/github/sponsors/SukramJ?style=for-the-badge&label=GitHub%20Sponsors&color=green
[sponsors]: https://github.com/sponsors/SukramJ
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-green.svg?style=for-the-badge

## License

This project is licensed under the MIT License. See LICENSE for details: https://github.com/sukramj/homematicip_local/blob/master/LICENSE
