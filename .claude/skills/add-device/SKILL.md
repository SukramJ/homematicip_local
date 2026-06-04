---
name: add-device
description: Add a new Homematic device type with DeviceProfileRegistry registration, custom data point class, and tests. Use when the user wants to add support for a new device model.
---

# Adding a New Device Type

Device-to-profile mappings are managed via `DeviceProfileRegistry`. Most new devices can use existing CustomDataPoint subclasses.

## Step 1: Register with DeviceProfileRegistry

Register in the appropriate entity module (e.g., `aiohomematic/model/custom/switch.py`, `climate.py`):

```python
# In aiohomematic/model/custom/switch.py (or appropriate module)
from aiohomematic.const import DataPointCategory, DeviceProfile, Parameter
from aiohomematic.model.custom.registry import DeviceProfileRegistry, ExtendedDeviceConfig

# Simple registration
DeviceProfileRegistry.register(
    category=DataPointCategory.SWITCH,
    models="HmIP-NEW-SWITCH",           # Single model or tuple of models
    data_point_class=CustomDpSwitch,     # Existing or new CustomDataPoint class
    profile_type=DeviceProfile.IP_SWITCH,
    channels=(3,),                        # Channel(s) where STATE lives
)

# With extended configuration (additional data points)
DeviceProfileRegistry.register(
    category=DataPointCategory.CLIMATE,
    models=("HmIP-NEW-THERMO", "HmIP-NEW-THERMO-2"),
    data_point_class=CustomDpIpThermostat,
    profile_type=DeviceProfile.IP_THERMOSTAT,
    channels=(1,),
    schedule_channel_no=1,
    extended=ExtendedDeviceConfig(
        additional_data_points={
            0: (Parameter.SOME_EXTRA_PARAM,),
        },
    ),
)
```

## Step 2: For Devices with Multiple Configurations

E.g., lock + button lock:

```python
from aiohomematic.model.custom.registry import DeviceConfig, DeviceProfileRegistry

DeviceProfileRegistry.register_multiple(
    category=DataPointCategory.LOCK,
    models="HmIP-NEW-LOCK",
    configs=(
        DeviceConfig(
            data_point_class=CustomDpIpLock,
            profile_type=DeviceProfile.IP_LOCK,
        ),
        DeviceConfig(
            data_point_class=CustomDpButtonLock,
            profile_type=DeviceProfile.IP_BUTTON_LOCK,
            channels=(0,),
        ),
    ),
)
```

## Step 3: Add a Calculated Data Point (if needed)

Create calculated class in `aiohomematic/model/calculated/`:

```python
"""Calculated data point."""

from __future__ import annotations

from aiohomematic.model.calculated.data_point import CalculatedDataPoint


class NewCalculation(CalculatedDataPoint):
    """Calculate derived value."""

    async def calculate_value(self) -> float:
        """Calculate and return derived value."""
        value1 = await self._get_source_value("PARAMETER1")
        value2 = await self._get_source_value("PARAMETER2")
        return value1 + value2
```

## Step 4: Add Tests

Add tests in `tests/test_model_*.py`.

## Reference

See `docs/developer/extension_points.md` for detailed instructions and more examples.
