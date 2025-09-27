# Naming of devices and entities

This document explains how Homematic(IP) Local for OpenCCU names devices and entities in Home Assistant. It is inspired by and largely aligned with the AIOhomematic naming documentation: https://github.com/SukramJ/aiohomematic/blob/devel/docs/naming.md. Where Homematic(IP) Local for OpenCCU behaves differently, this is highlighted.

## Terminology
- Device: A physical device registered on the CCU (or a hub-level pseudo device). In HA this is the Device entry in the device registry.
- Channel: A functional sub-unit of a device on the CCU. One device can have multiple channels. Channels map to data points which result in entities in HA.
- Data point: A parameter exposed by a device/channel (e.g. LEVEL, STATE). In HA, data points are represented as entities (either auto or custom mapped).
- Entity: A Home Assistant entity created from one or multiple data points.

## Sources for names
Names are taken from these sources, in the following order:
1. User-defined names from the CCU (rooms, device names, channel names).
2. Homematic logical names (device type, channel number) as fallback.
3. Home Assistant translation strings for parameter/entity type to present readable localized names.

## Device name in Home Assistant
- The HA device name is primarily the CCU device name.
- When “sub devices” are enabled and a device has sub devices (i.e. grouped channels), the HA device name might be extended with the group/master channel information:
  - If the entity’s channel belongs to a multi-group and there is a group master channel:
    - If the master channel has a non-empty, non-numeric name: use that name.
    - If the master channel name is numeric: use "{device name}-{master name}".
    - If the master channel has no name: use "{device name}-{group_no}".
- If sub devices are not enabled, the plain CCU device name is used.

This logic is implemented in AioHomematicGenericEntity._ha_device_name.

## Entity name in Home Assistant
Entity names are a combination of:
- The user/device/channel part coming from the CCU, and
- A translated parameter/entity type name provided by Home Assistant translations.

Rules:
- For calculated or generic entities:
  - Start from the data point’s name composed by the library (which is based on device/channel names and parameter names).
  - If sub devices are enabled and the device has sub devices, use only the parameter part from the name data as the base.
  - Replace the raw parameter name (e.g. "Level") with the translated name provided by HA (e.g. "Brightness" for lights) unless translations explicitly define an empty string (e.g. STATE, STATUS).
- For custom entities:
  - If the entity name starts with the device name, remove that device name to avoid duplication in HA’s UI.
  - Replace the raw parameter name with the HA translation similar to generic entities.
- If the resulting entity name equals the device name, the entity name is set to empty so that HA will display only the device name contextually.
- If the resulting entity name is empty, HA will use None (no explicit name), which results in default display derived from the device and platform.

This logic is implemented in AioHomematicGenericEntity.name.

### Removing the translated part
- Homematic(IP) Local for OpenCCU uses HA’s translation support to determine if the translated name should be removed entirely. If the translation text for the specific entity name key is an empty string, the translated part is omitted.

This logic is implemented in AioHomematicGenericEntity._do_remove_name.

## Use of device name as entity name
- Entities that do not have their own distinct name (after the above processing) are considered to "use the device name" in HA. This is exposed via the property use_device_name.

## Special cases
- Sub-device grouping: When enable_sub_devices is on and the device has grouped channels, the device name shown in HA will denote the group as described above. Entity names will use the parameter part only to avoid repeated device/group info.
- Custom entity mappings: Some complex devices map multiple data points into specialized entities (e.g., climate, cover). The naming rules still apply after removing duplicated device names and translating parameter names.

## Differences vs AIOhomematic
- Homematic(IP) Local for OpenCCU is the HA integration built on top of AIOhomematic. Naming is kept aligned with AIOhomematic’s documentation where feasible. Minor differences mainly stem from HA translation handling and the sub-device grouping enhancements described above.

## Examples
Note: These examples illustrate typical outcomes. Actual wording may vary with your language and device customizations on the CCU.

- Dimmer channel with device named "Livingroom Light", parameter LEVEL:
  - Device: "Livingroom Light"
  - Entity: "Brightness" (translated from LEVEL). If translations are empty for this entity type, the entity may have no explicit name.

- Switch channel with device "Garden Pump", parameter STATE, custom entity mapping to a switch:
  - Device: "Garden Pump"
  - Entity: "Switch" or no explicit name depending on translations; if custom entity name included the device name initially, that part is stripped.

- Multi-group device with base device name "RGB Controller", grouped master channel named "Shelf":
  - Device: "Shelf" (preferred, since master channel has non-empty non-numeric name)
  - Entity: "Brightness", "Color Temperature", etc., with parameter parts translated and device name removed from the entity portion to avoid duplication.

## Tips
- To control the names, prefer naming your devices and channels on the CCU. The integration will pick those up.
- If a translation appears odd or redundant, check HA’s translation files for the platform; some names are intentionally empty to let the UI focus on the device name.

