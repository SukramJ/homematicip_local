# Homematic(IP) Local for OpenCCU

> **⚠️ Development Branch:** This is the documentation for the development version. For the stable release documentation, see the [main branch README](https://github.com/sukramj/homematicip_local/blob/main/README.md).

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
- Minimum requirements: Home Assistant 2025.10.0+; for Homematic IP on CCU require at least CCU2 2.53.27 / CCU3 3.53.26.
- Useful links: [Installation guide](https://github.com/sukramj/homematicip_local/wiki/Installation), [Wiki](https://github.com/sukramj/aiohomematic/wiki), [Issues](https://github.com/sukramj/aiohomematic/issues), [Discussions](https://github.com/sukramj/aiohomematic/discussions), [Changelog](https://github.com/sukramj/homematicip_local/blob/master/changelog.md).

## Table of contents
- [Issues and discussions](#issues-and-discussions)
- [Documentation](#documentation)
- [Installation](#installation)
- [Device support](#device-support)
  - [Deactivated Entities](#deactivated-entities)
- [Requirements](#requirements)
  - [Hardware](#hardware)
  - [Firewall and required ports](#firewall-and-required-ports)
  - [Authentication](#authentication)
- [Configuration](#configuration)
- [Manual configuration steps](#manual-configuration-steps)
- [Auto-discovery](#auto-discovery)
  - [Configuration Variables](#configuration-variables)
- [Step 1: CCU Connection (Step 1 of 2)](#step-1-ccu-connection-step-1-of-2)
  - [Required Settings](#required-settings)
- [Automatic Backend Detection](#automatic-backend-detection)
- [Step 2: TLS & Interface Selection (Step 2 of 2)](#step-2-tls--interface-selection-step-2-of-2)
  - [TLS Settings](#tls-settings)
  - [Interface Selection](#interface-selection)
  - [Custom Port Configuration (Optional)](#custom-port-configuration-optional)
- [Finish or Configure Advanced](#finish-or-configure-advanced)
- [Advanced Options (Optional)](#advanced-options-optional)
  - [Callback Settings (Docker/Network)](#callback-settings-dockernetwork)
  - [System Variables & Programs](#system-variables--programs)
  - [Communication Settings](#communication-settings)
  - [MQTT Integration](#mqtt-integration)
  - [Device Behavior](#device-behavior)
  - [Expert Options](#expert-options)
- [Quick Setup Guide](#quick-setup-guide)
  - [Beginner Setup (HomematicIP Only)](#beginner-setup-homematicip-only)
  - [Advanced Setup (Mixed Devices + Custom Options)](#advanced-setup-mixed-devices--custom-options)
- [Reconfiguring the Integration](#reconfiguring-the-integration)
- [Options Flow (Configure)](#options-flow-configure)
- [System Variables & Programs](#system-variables--programs-1)
  - [Key Facts](#key-facts)
- [Understanding System Variables](#understanding-system-variables)
- [Two Modes: DEFAULT vs EXTENDED](#two-modes-default-vs-extended)
- [Filtering: Import Only What You Need](#filtering-import-only-what-you-need)
- [CCU Programs](#ccu-programs)
- [System Variables Quick Start](#system-variables-quick-start)
- [Important Notes](#important-notes)
- [Actions](#actions)
- [Events](#events)
- [Additional Information](#additional-information)
- [Understanding Entity States & Updates](#understanding-entity-states--updates)
- [Managing Devices & Entities](#managing-devices--entities)
- [Working with Device Parameters](#working-with-device-parameters)
- [Button Devices & Events](#button-devices--events)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)
- [Technical Details](#technical-details)
- [Updating Device Firmware](#updating-device-firmware)
- [OpenCCU Backup](#openccu-backup)
- [Adding New Devices (Pairing)](#adding-new-devices-pairing)
- [CUxD, CCU-Jack & MQTT Support](#cuxd-ccu-jack--mqtt-support)
- [Setting Up MQTT Support](#setting-up-mqtt-support)
- [CUxD & CCU-Jack Device Compatibility](#cuxd--ccu-jack-device-compatibility)
- [Troubleshooting](#troubleshooting)
- [Frequently Asked Questions](#frequently-asked-questions)
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
- **Contributing Guide**: See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines
- **Naming of devices and entities**: See [docs/naming.md](docs/naming.md)
- **API Behavioral Compatibility**: See [docs/BEHAVIORAL_COMPATIBILITY.md](docs/BEHAVIORAL_COMPATIBILITY.md)
- **Glossary of terms**: See [aiohomematic glossary](https://github.com/SukramJ/aiohomematic/blob/devel/docs/glossary.md)

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

The integration uses a streamlined 2-step configuration flow with optional advanced settings. This section explains each configuration option in detail.

**Configuration Flow Overview:**

```
Step 1: CCU Connection → Backend Detection → Step 2: TLS & Interfaces → Menu: Finish or Configure Advanced
```

---

## Step 1: CCU Connection (Step 1 of 2)

Enter your CCU credentials. The integration will automatically detect your backend type and available interfaces.

### Required Settings

| Setting | Description | Example | Notes |
|---------|-------------|---------|-------|
| **Instance Name** | Unique identifier for this integration instance | `ccu3` | Use lowercase letters and numbers only (a-z, 0-9). Must be unique if connecting multiple HA instances to the same CCU or connecting to multiple CCUs. |
| **Host** | Hostname or IP address of your CCU | `192.168.1.50` or `ccu3.local` | Make sure your CCU has a static IP or use a hostname that doesn't change. |
| **Username** | Admin username on your CCU | `Admin` | **Case sensitive!** User must have administrator privileges. |
| **Password** | Password for the admin user | `MySecurePass123` | **Case sensitive!** Only use allowed characters: `A-Z`, `a-z`, `0-9`, and `.!$():;#-` |

> **Tip:** After clicking "Submit", the integration automatically detects your CCU type and available interfaces. You'll see a brief progress indicator during detection.

---

## Automatic Backend Detection

After entering your connection settings, the integration runs **automatic backend detection**:

| What's Detected | Description |
|-----------------|-------------|
| **Backend Type** | CCU2, CCU3, OpenCCU, Debmatic, or Homegear |
| **Available Interfaces** | HmIP-RF, BidCos-RF, BidCos-Wired, Virtual Devices, CUxD, CCU-Jack |
| **TLS Configuration** | Whether your CCU uses encrypted connections |
| **HTTPS Redirect** | Whether HTTP is redirected to HTTPS |

**What happens:**
1. ✅ A progress screen shows "Detecting backend type and available interfaces..."
2. ✅ Detected interfaces are **pre-selected** in Step 2
3. ✅ TLS is **automatically enabled** if your CCU uses HTTPS
4. ❌ If detection fails, you're returned to Step 1 with a clear error message

**Common detection errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| `Authentication failed` | Wrong username/password | Verify credentials are correct (case-sensitive) |
| `Cannot connect` | Network issue or wrong host | Check CCU IP address, ensure it's powered on |
| `Detection failed` | CCU not responding properly | Verify user has admin privileges |

---

## Step 2: TLS & Interface Selection (Step 2 of 2)

Configure TLS settings and select which device types to integrate. Interfaces detected in the previous step are **pre-selected**.

### TLS Settings

| Setting | Default | When to Use |
|---------|---------|-------------|
| **Use TLS** | Auto-detected | Enable if your CCU uses HTTPS. Ports automatically adjust (e.g., 2010 → 42010). |
| **Verify TLS** | `false` | Enable only if your CCU has a valid SSL certificate (not self-signed). |

### Interface Selection

Enable only the interfaces your CCU actually uses:

| Interface | Enable If You Have... | Default Port | TLS Port |
|-----------|----------------------|--------------|----------|
| **HomematicIP (HmIP-RF)** | HomematicIP wireless or wired devices | 2010 | 42010 |
| **Homematic (BidCos-RF)** | Classic Homematic wireless devices | 2001 | 42001 |
| **Homematic Wired (BidCos-Wired)** | Classic Homematic wired devices | 2000 | 42000 |
| **Heating Groups (Virtual Devices)** | Thermostat groups configured in CCU | 9292 | 49292 |
| **CUxD** | CUxD add-on installed | - | - |
| **CCU-Jack** | CCU-Jack software installed | - | - |

### Custom Port Configuration (Optional)

**Ports are automatically set** based on your TLS setting. Only enable **"Configure custom ports"** if:
- Your CCU uses non-standard ports
- Connection fails with default ports (the port page appears automatically in this case)

> **Note:** If the default ports don't work, the integration automatically shows the port configuration page so you can adjust them.

**Common Interface Configurations:**

| Your Devices | Interfaces to Enable |
|--------------|---------------------|
| Only HomematicIP devices | ✓ HomematicIP only |
| HomematicIP + classic Homematic | ✓ HomematicIP + ✓ Homematic (BidCos-RF) |
| With thermostat groups | Add ✓ Heating Groups |
| With CUxD or CCU-Jack | Add respective interface + configure MQTT later |

---

## Finish or Configure Advanced

After Step 2, you see a menu with two options:

| Option | When to Choose |
|--------|----------------|
| **Finish setup** | ✅ Recommended for most users. Uses sensible defaults. |
| **Configure advanced options** | Only if you need: callback settings (Docker), MQTT, marker filtering, or expert options |

> **Tip:** You can always access advanced options later via **Configure** in the integration settings.

---

## Advanced Options (Optional)

Only accessible if you choose "Configure advanced options" in the menu. Most users don't need these settings.

### Callback Settings (Docker/Network)

Only configure these if Home Assistant can't receive state updates from your CCU:

| Setting | Purpose | When to Use |
|---------|---------|-------------|
| **Callback Host** | IP address the CCU uses to reach HA | Required if HA runs in Docker with custom networking |
| **Callback Port (XML-RPC)** | Port for state updates from CCU | Required in Docker setups with port forwarding |

**Docker Users:**
- **Recommended:** Use `network_mode: host` in your Docker configuration
- **Alternative:** Set Callback Host to your Docker host's IP and configure port forwarding

### System Variables & Programs

| Setting | Default | Description |
|---------|---------|-------------|
| **Enable System Variable Scan** | `true` | Fetch system variables from CCU |
| **System Variable Markers** | All | Filter which variables to import (HAHM, MQTT, HX, INTERNAL) |
| **Enable Program Scan** | `true` | Fetch programs from CCU |
| **Program Markers** | All except INTERNAL | Filter which programs to import |
| **Scan Interval** | 30 seconds | How often to poll for changes |

**About Markers:**
- **HAHM** - Creates writable entities (switch, select, number, text)
- **MQTT** - Enables push updates via MQTT (requires CCU-Jack)
- **HX** - Custom marker for your own filtering
- **INTERNAL** - Includes CCU-internal variables/programs

### Communication Settings

| Setting | Default | When to Change |
|---------|---------|----------------|
| **System Notifications** | `true` | Don't disable - shows important network warnings |
| **Listen on All IPs** | `false` | Only for Docker-on-Mac/Windows with virtualization issues |

### MQTT Integration

| Setting | Default | Description |
|---------|---------|-------------|
| **Enable MQTT** | `false` | For CUxD and CCU-Jack device events |
| **MQTT Prefix** | _(empty)_ | Set if using MQTT Bridge |

**Prerequisites:** HA connected to MQTT broker, CCU-Jack installed

### Device Behavior

| Setting | Default | Description |
|---------|---------|-------------|
| **Enable Sub-Devices** | `false` | Create separate devices for each channel |
| **Use Group Channel for Cover State** | `true` | Cover groups use state channel level |

### Expert Options

| Setting | Description |
|---------|-------------|
| **Unignore Parameters** | Add filtered device parameters as entities |
| **Optional Settings** | Debug/analytics features (development only) |

---

## Quick Setup Guide

### Beginner Setup (HomematicIP Only)

Most users only need HomematicIP devices. Follow these simple steps:

**Step 1 - Enter CCU Connection:**
```
Instance Name: OpenCCU-Prod
Host:          192.168.1.50  (your CCU's IP address)
Username:      Admin
Password:      (your CCU admin password)
```

**Automatic Detection:**
- Wait for the progress indicator to complete
- The integration detects your CCU type and available interfaces

**Step 2 - Verify Settings:**
- TLS: Leave as detected (usually `false`)
- Interfaces: HomematicIP/ BidCos-RF / Bidcos-Wired could be pre-selected ✓
- Custom ports: Leave unchecked

**Finish:**
- Click **"Finish setup"**
- Done! Your devices will appear within seconds.

---

### Advanced Setup (Mixed Devices + Custom Options)

For users with multiple device types or special network setups:

**Step 1 - Enter CCU Connection:**
```
Instance Name: OpenCCU-Prod  (unique name for your setup)
Host:          192.168.1.50
Username:      Admin
Password:      (your password)
```

**Step 2 - Configure Interfaces:**
- TLS: Enable if your CCU uses HTTPS
- Select all interfaces you use:
  - ✓ HomematicIP
  - ✓ Homematic (BidCos-RF)
  - ✓ Heating Groups (if you have thermostat groups)

**Choose "Configure advanced options" → Then:**
```
Callback Host:    (leave empty, unless Docker with custom network)
Enable MQTT:      true (if using CUxD or CCU-Jack)
Sysvar Markers:   Select HAHM (for writable system variables)
Scan Interval:    30
```

**Click Submit → Done!**

---

## Reconfiguring the Integration

Update your CCU connection without removing and re-adding the integration:

1. Go to **Settings** → **Devices & Services**
2. Find **Homematic(IP) Local for OpenCCU**
3. Click the **three-dot menu (⋮)** → **Reconfigure**
4. **Step 1:** Update host, username, or password
5. **Step 2:** Update TLS and interface settings
6. Submit → Integration reloads with new settings

**What Reconfigure changes:**
- ✅ Host/IP address
- ✅ Username and password
- ✅ TLS settings
- ✅ Interface selection
- ✅ Custom ports

**What Reconfigure does NOT change:**
- ❌ Advanced options (use **Configure** instead)
- ❌ Instance name (must delete and re-add)

---

## Options Flow (Configure)

Use **Configure** (not Reconfigure) to access all settings via a menu:

1. Go to **Settings** → **Devices & Services**
2. Find **Homematic(IP) Local for OpenCCU**
3. Click **Configure**

| Menu Option | What You Can Change |
|-------------|---------------------|
| **Connection** | Host, username, password |
| **TLS & Interfaces** | TLS settings, interface selection, custom ports |
| **Programs & Sysvars** | System variable/program scanning and markers |
| **Advanced Settings** | Callbacks, MQTT, device behavior, unignore parameters |

> **When to use Configure vs Reconfigure:**
> - **Reconfigure:** Quick updates to connection/interface settings
> - **Configure:** Access to all settings including advanced options

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

## System Variables Quick Start

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
- Each weekday has a `base_temperature` and a list of `periods`
- You specify only the active heating/cooling periods with `starttime`, `endtime`, and `temperature` (lowercase keys)
- The system automatically fills gaps with `base_temperature`
- All time periods outside your specified slots use `base_temperature`
- The system converts everything to the required 13-slot format automatically

**Note:** Since version 2.0.0, simple schedules use lowercase keys for better JSON serialization support.

**Example:** See [sample](#sample-for-set_schedule_simple_profile) below for the full data structure.

### `homematicip_local.set_schedule_simple_weekday`

__Disclaimer: Too much writing to the device could kill your device's storage.__

Sends the schedule for a single weekday of a climate profile using a **simplified format**.

**Why use this?** Instead of managing 13 slots, you only define the specific temperature periods you need.

**How it works:**
1. You provide a list of temperature periods with `starttime`, `endtime`, and `temperature` (lowercase keys)
2. You specify a `base_temperature` for all times not covered by your periods
3. The system automatically:
   - Sorts your periods chronologically
   - Fills gaps between periods with `base_temperature`
   - Converts to the required 13-slot format
   - Validates all ranges and sequences

**Note:** Since version 2.0.0, simple schedules use lowercase keys for better JSON serialization support.

**Example:**
```yaml
base_temperature: 18.0
simple_weekday_list:
  - starttime: "06:00"
    endtime: "08:00"
    temperature: 21.0
  - starttime: "17:00"
    endtime: "22:00"
    temperature: 21.0
```

This creates:
- 00:00-06:00: 18.0°C (base_temperature)
- 06:00-08:00: 21.0°C (your first period)
- 08:00-17:00: 18.0°C (base_temperature fills gap)
- 17:00-22:00: 21.0°C (your second period)
- 22:00-24:00: 18.0°C (base_temperature)

See the [sample](#sample-for-set_schedule_simple_weekday) below for a complete example. 

### `homematicip_local.get_variable_value`

Get the value variable from your Homematic hub.

### `homematicip_local.set_variable_value`

Set the value of a variable on your Homematic hub.

Value lists accept the 0-based list position or the value as input.

For booleans the following values can be used:

- 'true', 'on', '1', 1 -> True
- 'false', 'off', '0', 0 -> False

### `homematicip_local.turn_on_siren`

Turn siren on. Siren can be disabled by siren.turn_off.

**Note:** Since version 2.0.0, the integration automatically creates **Select entities** for siren tone and light pattern selection. These entities:
- Store selections locally (persist across Home Assistant restarts)
- Are grouped under the siren device
- Appear in the "Configuration" entity category
- Replace the need for manual [InputHelper creation](https://github.com/sukramj/aiohomematic/blob/devel/docs/input_select_helper.md#siren)

Available automatic select entities:
- **Siren Tone** (`select.<device>_acoustic_alarm_selection`) - Choose the alarm tone
- **Siren Light Pattern** (`select.<device>_optical_alarm_selection`) - Choose the light pattern

The selected values are automatically used when calling siren services or using the siren entity.

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

## OpenCCU Backup

This integration provides functionality to create and download backups directly from Home Assistant.

> **⚠️ Important:** This feature is **only available for OpenCCU** (formerly RaspberryMatic). It is **not supported** on original CCU-based systems due to firmware limitations.

| Supported     | Not Supported |
|---------------|---------------|
| ✅ OpenCCU    | ❌ CCU2       |
|               | ❌ CCU3       |
|               | ❌ Debmatic   |
|               | ❌ piVCCU     |

### Creating Backups

**Two methods are available:**

| Method | How to Use                                          | Best For |
|--------|-----------------------------------------------------|----------|
| **Button Entity** | Click "Create Backup" button on your OpenCCU device | Quick manual backups, dashboard integration |
| **Action** | Call `homematicip_local.create_ccu_backup`          | Automations, scheduled backups |

### Backup Storage

Backups are saved to a configurable directory within Home Assistant's storage:

- **Location:** `<HA_storage>/homematicip_local/backup/`
- **File format:** `ccu_backup_<central_name>_<YYYYMMDD_HHMMSS>.sbk`

### Using the Backup Action

```yaml
action: homematicip_local.create_ccu_backup
data:
  entry_id: YOUR_ENTRY_ID
```

**Returns:**
```yaml
success: true
path: "/config/.storage/homematicip_local/backup/ccu_backup_raspberrymatic_20251203_143022.sbk"
filename: "ccu_backup_raspberrymatic_20251203_143022.sbk"
size: 12345678
```

### Automating Backups

**Example: Weekly backup automation**

```yaml
automation:
  - alias: "Weekly OpenCCU Backup"
    trigger:
      - platform: time
        at: "03:00:00"
    condition:
      - condition: time
        weekday:
          - sun
    action:
      - action: homematicip_local.create_ccu_backup
        data:
          entry_id: YOUR_ENTRY_ID
```

**Note:** Backup creation can take several minutes depending on your OpenCCU configuration size.

---

## Adding New Devices (Pairing)

New devices are added to Home Assistant through a **controlled repair notification process**. This ensures devices get proper names and entity IDs from the start.

### Why Repair Notifications?

When you pair a new device with your CCU, it typically has a technical address like `VCU1234567`. If the integration created entities immediately, you'd get ugly entity IDs like `sensor.vcu1234567_temperature`.

The repair notification gives you the chance to:
- ✅ Name the device properly before entities are created
- ✅ Get clean entity IDs like `sensor.living_room_thermostat_temperature`
- ✅ Control exactly when devices appear in Home Assistant

### Step-by-Step: Adding a New Device

**1. Pair the device with your CCU**

Use your CCU's web interface to pair the new device:
- CCU3/OpenCCU: Settings → Devices → Teach-in device
- Follow the device's pairing instructions (usually pressing a button)

**2. (Recommended) Name the device in CCU**

While still in the CCU interface:
- Give the device a meaningful name (e.g., "Living Room Thermostat")
- Assign it to a room (this becomes the HA area)

> **Tip:** Naming in CCU first is easier because you can use spaces and special characters. The integration will use this name.

**3. Check Home Assistant Repairs**

After pairing, Home Assistant shows a repair notification:

1. Go to **Settings** → **System** → **Repairs**
2. You'll see: "Device creation of [ADDRESS] delayed on [INTERFACE]"
3. Click on the notification

**4. Confirm or Name the Device**

In the repair dialog:

| If you... | Then... |
|-----------|---------|
| Named the device in CCU | Leave the name field **empty** → Click Submit |
| Didn't name in CCU | Enter a name (e.g., "Kitchen Motion Sensor") → Click Submit |

**5. Done!**

The device and all its entities are now created in Home Assistant with proper names.

### Example: Adding a Temperature Sensor

```
CCU: Pair device HmIP-STHD → Address: VCU0012345
CCU: Name it "Bedroom Thermostat", assign to room "Bedroom"
HA:  Repair notification appears
HA:  Click repair → Leave name empty → Submit
HA:  Device "Bedroom Thermostat" created in area "Bedroom"
HA:  Entities: climate.bedroom_thermostat, sensor.bedroom_thermostat_temperature, etc.
```

### Naming Options Comparison

| Method | Where to Name | Result |
|--------|---------------|--------|
| **Option A (Recommended)** | Name in CCU first | CCU name is used, syncs both systems |
| **Option B** | Name in HA repair dialog | Name only in HA, CCU keeps technical address |
| **Option C** | Skip naming | Technical address used (not recommended) |

### Room/Area Assignment

| CCU Room Configuration | HA Area Assignment |
|------------------------|-------------------|
| Device assigned to one room | ✅ Area matches CCU room |
| Device assigned to multiple rooms | ❌ No area (HA only allows one) |
| No room assigned | ❌ No area assigned |

> **Note:** You can always change the area later in HA device settings.

### Troubleshooting New Devices

**Device doesn't appear as repair notification:**
- Wait 30-60 seconds after pairing
- Check if the device is visible in CCU
- Reload the integration (Settings → Integrations → Reload)

**Wrong name was used:**
1. Delete the device in HA (Settings → Devices → Select device → Delete)
2. Rename in CCU
3. Reload integration → New repair notification appears

**Device appears with technical address:**
- This happens if you confirmed without entering a name
- Delete and re-add as described above

---

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

Before opening an issue, work through this troubleshooting guide:

### First Steps Checklist

| Check | How to Verify |
|-------|---------------|
| ✅ HA logs reviewed | Settings → System → Logs → Filter: `homematicip_local`, `aiohomematic` |
| ✅ Ports open | Can reach CCU from HA (test with ping, telnet to port 2010) |
| ✅ CCU reachable | CCU web interface accessible from same network |
| ✅ Admin user | CCU user has administrator privileges |
| ✅ Valid password | Only characters: A-Z, a-z, 0-9 and `.!$():;#-` |

### Docker-Specific Issues

| Problem | Solution |
|---------|----------|
| No state updates | Set `callback_host` to Docker host IP in Advanced Options |
| Connection refused | Use `network_mode: host` (recommended) |
| Multiple instances conflict | Ensure unique `instance_name` per HA instance |

### Common Problems & Solutions

**Entity shows "Unavailable"**
1. Entity might be **disabled** → Settings → Entities → Enable it
2. Device offline → Check CCU if device is reachable
3. After CCU restart → Wait for device to report in (battery devices: hours)

**Devices not appearing**
1. New devices appear as **Repair notifications** → Check Settings → System → Repairs
2. Reload integration → Settings → Integrations → Reload
3. Check interface is enabled → Reconfigure → Verify correct interfaces selected

**Auto-discovery keeps appearing**
1. Click **Ignore** on the discovery notification
2. Or reconfigure the existing integration entry
3. Restart Home Assistant

**After CCU firmware update**
1. Restart Home Assistant
2. Reload the integration
3. Check for changed ports or interfaces

### Getting Help

If you can't resolve the issue:

1. **Search existing issues:** [GitHub Issues](https://github.com/sukramj/aiohomematic/issues)
2. **Ask in discussions:** [GitHub Discussions](https://github.com/sukramj/aiohomematic/discussions)
3. **Open an issue** with:
   - HA version and integration version
   - CCU type and firmware version
   - Relevant log entries
   - Steps to reproduce

---

## Frequently Asked Questions

**Q: Entity shows "unavailable" - why?**

The entity might be disabled. Go to Settings → Entities → find the entity → click Enable.

---

**Q: Button presses don't trigger my automation**

HomematicIP button devices need central links enabled. See [Enabling Button Events](#enabling-button-events) section.

---

**Q: My device isn't listed in the button events documentation**

That's fine! The documentation shows examples. Any device with physical buttons will emit events - if you can press it, it works.

---

**Q: What are APPARENT_TEMPERATURE, DEW_POINT, FROST_POINT sensors?**

These are [calculated sensors](https://github.com/SukramJ/aiohomematic/blob/devel/docs/calculated_climate_sensors.md) derived from existing device parameters to provide additional information.

---

**Q: New device added to CCU but doesn't appear in HA**

New devices create a **repair notification** instead of appearing automatically:
1. Go to **Settings** → **System** → **Repairs**
2. Click the notification for your new device
3. Enter a name and confirm

See [Adding New Devices](#adding-new-devices-pairing) for details.

---

**Q: How do I change a device name?**

| Goal | Method |
|------|--------|
| Change name in HA only | Settings → Devices → Select device → Edit name |
| Sync name from CCU | Rename in CCU → Reload integration |
| Change entity ID too | Delete device in HA → Rename in CCU → Reload integration |

---

**Q: My CCU has many system variables but I only see a few**

By default, system variables are imported as **disabled entities**. To see them:
1. Settings → Entities → Show disabled entities
2. Enable the ones you need

Or use **markers** to auto-enable specific variables. See [System Variables & Programs](#system-variables--programs).

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

**What this does:** Sets profile P1 with heating periods for each weekday. Each weekday has its own base temperature and periods. All times not covered by periods use the weekday's base temperature.

**Note:** Since version 2.0.0, the simple schedule format uses lowercase keys (`starttime`, `endtime`, `temperature`) for better JSON serialization support.

```yaml
---
action: homematicip_local.set_schedule_simple_profile
target:
  entity_id: climate.heizkorperthermostat_db
data:
  profile: P1
  simple_profile_data:
    MONDAY:
      base_temperature: 16.0  # Base temp for Monday
      periods:
        # Morning warm-up: 05:00-06:00 at 17°C
        - starttime: "05:00"
          endtime: "06:00"
          temperature: 17.0
        # Daytime: 09:00-15:00 at 17°C
        - starttime: "09:00"
          endtime: "15:00"
          temperature: 17.0
        # Evening: 19:00-22:00 at 22°C
        - starttime: "19:00"
          endtime: "22:00"
          temperature: 22.0
      # All other times use base_temperature 16.0°C
    TUESDAY:
      base_temperature: 16.0  # Base temp for Tuesday
      periods:
        - starttime: "05:00"
          endtime: "06:00"
          temperature: 17.0
        - starttime: "09:00"
          endtime: "15:00"
          temperature: 17.0
        - starttime: "19:00"
          endtime: "22:00"
          temperature: 22.0
    # Add other weekdays as needed (WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY)
```

### Sample for set_schedule_simple_weekday

Send a simple climate schedule for Monday only:

**What this does:** Sets Monday's schedule for profile P3. Three heating periods are defined. The base temperature (16°C) is used for all other times.

**Note:** Since version 2.0.0, the simple schedule format uses lowercase keys (`starttime`, `endtime`, `temperature`) for better JSON serialization support.

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
    - starttime: "05:00"
      endtime: "06:00"
      temperature: 17.0
    # Daytime: 09:00-15:00 at 17°C
    - starttime: "09:00"
      endtime: "15:00"
      temperature: 17.0
    # Evening: 19:00-22:00 at 22°C
    - starttime: "19:00"
      endtime: "22:00"
      temperature: 22.0
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

**Getting Help:**
- **Issues**: Report bugs at https://github.com/sukramj/aiohomematic/issues
- **Discussions**: Ask questions at https://github.com/sukramj/aiohomematic/discussions
- **Wiki**: Find additional information at https://github.com/sukramj/aiohomematic/wiki

**Contributing:**
- **Contributing Guide**: See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development setup, code standards, and workflow
- **Pull Requests**: Welcome! Please open an issue or discussion first for larger changes
- **Wiki Contributions**: Help improve documentation at https://github.com/sukramj/aiohomematic/wiki


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
