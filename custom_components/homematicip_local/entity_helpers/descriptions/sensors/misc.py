"""Miscellaneous sensor entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from custom_components.homematicip_local.entity_helpers.base import HmSensorEntityDescription
from custom_components.homematicip_local.entity_helpers.factories import (
    diagnostic_sensor,
    enum_sensor,
    measurement_sensor,
    simple_sensor,
)
from custom_components.homematicip_local.entity_helpers.registry import EntityDescriptionRule
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import PERCENTAGE, SIGNAL_STRENGTH_DECIBELS_MILLIWATT, EntityCategory, UnitOfTime

MISC_SENSOR_RULES: list[EntityDescriptionRule] = [
    # RSSI signal strength
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("RSSI_DEVICE", "RSSI_PEER"),
        description=diagnostic_sensor(
            key="RSSI",
            device_class=SensorDeviceClass.SIGNAL_STRENGTH,
            unit=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        ),
    ),
    # Carrier sense level
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("CARRIER_SENSE_LEVEL",),
        description=diagnostic_sensor(
            key="CARRIER_SENSE_LEVEL",
            unit=PERCENTAGE,
            icon="mdi:radio-tower",
            enabled_default=True,
        ),
    ),
    # Duty cycle level
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("DUTY_CYCLE_LEVEL",),
        description=diagnostic_sensor(
            key="DUTY_CYCLE_LEVEL",
            unit=PERCENTAGE,
            icon="mdi:radio-tower",
            enabled_default=True,
        ),
    ),
    # IP Address
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("IP_ADDRESS",),
        description=simple_sensor(
            key="IP_ADDRESS",
            entity_category=EntityCategory.DIAGNOSTIC,
            icon="mdi:ip-network",
        ),
    ),
    # Code ID
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("CODE_ID",),
        description=simple_sensor(
            key="CODE_ID",
        ),
    ),
    # Direction / Activity state
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("ACTIVITY_STATE", "DIRECTION"),
        description=enum_sensor(
            key="DIRECTION",
            translation_key="direction",
        ),
    ),
    # Door state
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("DOOR_STATE",),
        description=enum_sensor(
            key="DOOR_STATE",
            translation_key="door_state",
        ),
    ),
    # Lock state
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("LOCK_STATE",),
        description=enum_sensor(
            key="LOCK_STATE",
            translation_key="lock_state",
        ),
    ),
    # Smoke detector alarm status
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("SMOKE_DETECTOR_ALARM_STATUS",),
        description=enum_sensor(
            key="SMOKE_DETECTOR_ALARM_STATUS",
            translation_key="smoke_detector_alarm_status",
        ),
    ),
    # VALUE (generic measurement)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("VALUE",),
        description=measurement_sensor(
            key="VALUE",
        ),
    ),
    # Device-specific: WKP code state
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("CODE_STATE",),
        devices=("HmIP-WKP",),
        priority=10,
        description=enum_sensor(
            key="WKP_CODE_STATE",
            translation_key="wkp_code_state",
        ),
    ),
    # Device-specific: Tri-state sensors (window handles, etc.)
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("STATE",),
        devices=("HmIP-SRH", "HmIP-STV", "HM-Sec-RHS", "HM-Sec-xx", "ZEL STG RM FDK"),
        priority=10,
        description=enum_sensor(
            key="TRI_STATE",
            translation_key="tri_state",
        ),
    ),
    # Device-specific: HM-Sec-Key direction
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("DIRECTION",),
        devices=("HM-Sec-Key",),
        priority=10,
        description=enum_sensor(
            key="SEC-KEY_DIRECTION",
            translation_key="sec_direction",
        ),
    ),
    # Device-specific: HM-Sec-Key error
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("ERROR",),
        devices=("HM-Sec-Key",),
        priority=10,
        description=enum_sensor(
            key="SEC-KEY_ERROR",
            translation_key="sec_key_error",
        ),
    ),
    # Device-specific: HM-Sec-WDS state
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("STATE",),
        devices=("HM-Sec-WDS",),
        priority=10,
        description=enum_sensor(
            key="STATE",
            translation_key="sec_wds_state",
        ),
    ),
    # Device-specific: HM-Sec-Win status
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("STATUS",),
        devices=("HM-Sec-Win",),
        priority=10,
        description=enum_sensor(
            key="SEC-WIN_STATUS",
            translation_key="sec_win_status",
        ),
    ),
    # Device-specific: HM-Sec-Win direction
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("DIRECTION",),
        devices=("HM-Sec-Win",),
        priority=10,
        description=enum_sensor(
            key="SEC-WIN_DIRECTION",
            translation_key="sec_direction",
        ),
    ),
    # Device-specific: HM-Sec-Win error
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("ERROR",),
        devices=("HM-Sec-Win",),
        priority=10,
        description=enum_sensor(
            key="SEC-WIN_ERROR",
            translation_key="sec_win_error",
        ),
    ),
    # Device-specific: Smoke detector time of operation
    EntityDescriptionRule(
        category=DataPointCategory.SENSOR,
        parameters=("TIME_OF_OPERATION",),
        devices=("HmIP-SWSD",),
        priority=10,
        description=HmSensorEntityDescription(
            key="TIME_OF_OPERATION",
            device_class=SensorDeviceClass.DURATION,
            entity_category=EntityCategory.DIAGNOSTIC,
            entity_registry_enabled_default=False,
            multiplier=1 / 86400,
            native_unit_of_measurement=UnitOfTime.DAYS,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
    ),
]
