"""Binary sensor entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from ..factories import binary_sensor, diagnostic_binary_sensor
from ..registry import EntityDescriptionRule

BINARY_SENSOR_RULES: list[EntityDescriptionRule] = [
    # Safety/Alarm sensors
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("ALARMSTATE",),
        description=binary_sensor(
            key="ALARMSTATE",
            device_class=BinarySensorDeviceClass.SAFETY,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("ACOUSTIC_ALARM_ACTIVE",),
        description=binary_sensor(
            key="ACOUSTIC_ALARM_ACTIVE",
            device_class=BinarySensorDeviceClass.SAFETY,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("OPTICAL_ALARM_ACTIVE",),
        description=binary_sensor(
            key="OPTICAL_ALARM_ACTIVE",
            device_class=BinarySensorDeviceClass.SAFETY,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("EMERGENCY_OPERATION",),
        description=binary_sensor(
            key="EMERGENCY_OPERATION",
            device_class=BinarySensorDeviceClass.SAFETY,
            enabled_default=False,
        ),
    ),
    # Problem sensors
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("BLOCKED_PERMANENT", "BLOCKED_TEMPORARY"),
        description=diagnostic_binary_sensor(
            key="BLOCKED",
            device_class=BinarySensorDeviceClass.PROBLEM,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("BURST_LIMIT_WARNING",),
        description=diagnostic_binary_sensor(
            key="BURST_LIMIT_WARNING",
            device_class=BinarySensorDeviceClass.PROBLEM,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("DUTYCYCLE", "DUTY_CYCLE"),
        description=diagnostic_binary_sensor(
            key="DUTY_CYCLE",
            device_class=BinarySensorDeviceClass.PROBLEM,
            icon="mdi:radio-tower",
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("DEW_POINT_ALARM",),
        description=binary_sensor(
            key="DEW_POINT_ALARM",
            device_class=BinarySensorDeviceClass.PROBLEM,
            enabled_default=False,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("ERROR_JAMMED",),
        description=binary_sensor(
            key="ERROR_JAMMED",
            device_class=BinarySensorDeviceClass.PROBLEM,
            enabled_default=False,
        ),
    ),
    # Battery
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("LOWBAT", "LOW_BAT", "LOWBAT_SENSOR"),
        description=diagnostic_binary_sensor(
            key="LOW_BAT",
            device_class=BinarySensorDeviceClass.BATTERY,
            enabled_default=True,  # Battery is important
        ),
    ),
    # Heat
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("HEATER_STATE",),
        description=binary_sensor(
            key="HEATER_STATE",
            device_class=BinarySensorDeviceClass.HEAT,
        ),
    ),
    # Moisture
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("MOISTURE_DETECTED",),
        description=binary_sensor(
            key="MOISTURE_DETECTED",
            device_class=BinarySensorDeviceClass.MOISTURE,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("RAINING",),
        description=binary_sensor(
            key="RAINING",
            device_class=BinarySensorDeviceClass.MOISTURE,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("WATERLEVEL_DETECTED",),
        description=binary_sensor(
            key="WATERLEVEL_DETECTED",
            device_class=BinarySensorDeviceClass.MOISTURE,
        ),
    ),
    # Motion
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("MOTION",),
        description=binary_sensor(
            key="MOTION",
            device_class=BinarySensorDeviceClass.MOTION,
        ),
    ),
    # Presence
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("PRESENCE_DETECTION_STATE",),
        description=binary_sensor(
            key="PRESENCE_DETECTION_STATE",
            device_class=BinarySensorDeviceClass.PRESENCE,
        ),
    ),
    # Power
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("POWER_MAINS_FAILURE",),
        description=binary_sensor(
            key="POWER_MAINS_FAILURE",
            device_class=BinarySensorDeviceClass.POWER,
        ),
    ),
    # Running/Process
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("PROCESS", "WORKING"),
        description=binary_sensor(
            key="PROCESS",
            device_class=BinarySensorDeviceClass.RUNNING,
        ),
    ),
    # Tamper/Sabotage
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("SABOTAGE", "SABOTAGE_STICKY"),
        description=diagnostic_binary_sensor(
            key="SABOTAGE",
            device_class=BinarySensorDeviceClass.TAMPER,
        ),
    ),
    # Window
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("WINDOW_STATE",),
        description=binary_sensor(
            key="WINDOW_STATE",
            device_class=BinarySensorDeviceClass.WINDOW,
        ),
    ),
    # Device-specific: DSD-PCB occupancy
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("STATE",),
        devices=("HmIP-DSD-PCB",),
        priority=10,
        description=binary_sensor(
            key="STATE",
            device_class=BinarySensorDeviceClass.OCCUPANCY,
        ),
    ),
    # Device-specific: Contact sensors (SCI, FCI)
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("STATE",),
        devices=("HmIP-SCI", "HmIP-FCI1", "HmIP-FCI6"),
        priority=10,
        description=binary_sensor(
            key="STATE",
            device_class=BinarySensorDeviceClass.OPENING,
        ),
    ),
    # Device-specific: Smoke detector
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("STATE",),
        devices=("HM-Sec-SD",),
        priority=10,
        description=binary_sensor(
            key="STATE",
            device_class=BinarySensorDeviceClass.SMOKE,
        ),
    ),
    # Device-specific: Window/Door sensors
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("STATE",),
        devices=(
            "HmIP-SWD",
            "HmIP-SWDO",
            "HmIP-SWDM",
            "HM-Sec-SC",
            "HM-SCI-3-FM",
            "ZEL STG RM FFK",
        ),
        priority=10,
        description=binary_sensor(
            key="STATE",
            device_class=BinarySensorDeviceClass.WINDOW,
        ),
    ),
    # Device-specific: Rain detector
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("STATE",),
        devices=("HM-Sen-RD-O",),
        priority=10,
        description=binary_sensor(
            key="STATE",
            device_class=BinarySensorDeviceClass.MOISTURE,
        ),
    ),
    # Device-specific: HM-Sec-Win working state
    EntityDescriptionRule(
        category=DataPointCategory.BINARY_SENSOR,
        parameters=("WORKING",),
        devices=("HM-Sec-Win",),
        priority=10,
        description=binary_sensor(
            key="WORKING",
            device_class=BinarySensorDeviceClass.RUNNING,
            enabled_default=False,
        ),
    ),
]
