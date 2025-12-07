"""Hub-specific entity description rules."""

from __future__ import annotations

from aiohomematic.const import DataPointCategory
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy, UnitOfLength, UnitOfTime

from ..base import HmButtonEntityDescription, HmSensorEntityDescription
from ..registry import EntityDescriptionRule

HUB_RULES: list[EntityDescriptionRule] = [
    # Hub buttons
    EntityDescriptionRule(
        category=DataPointCategory.HUB_BUTTON,
        var_name_contains="INSTALL_MODE_HMIP_BUTTON",
        description=HmButtonEntityDescription(
            key="INSTALL_MODE_HMIP_BUTTON",
            translation_key="install_mode_hmip_button",
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.HUB_BUTTON,
        var_name_contains="INSTALL_MODE_BIDCOS_BUTTON",
        description=HmButtonEntityDescription(
            key="INSTALL_MODE_BIDCOS_BUTTON",
            translation_key="install_mode_bidcos_button",
        ),
    ),
    # Hub sensors - System messages
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="ALARM_MESSAGES",
        description=HmSensorEntityDescription(
            key="ALARM_MESSAGES",
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="SERVICE_MESSAGES",
        description=HmSensorEntityDescription(
            key="SERVICE_MESSAGES",
            state_class=SensorStateClass.MEASUREMENT,
        ),
    ),
    # Hub sensors - Install mode
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="INSTALL_MODE_HMIP",
        description=HmSensorEntityDescription(
            key="INSTALL_MODE_HMIP",
            translation_key="install_mode_hmip",
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="INSTALL_MODE_BIDCOS",
        description=HmSensorEntityDescription(
            key="INSTALL_MODE_BIDCOS",
            translation_key="install_mode_bidcos",
        ),
    ),
    # Hub sensors - Inbox
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="INBOX",
        description=HmSensorEntityDescription(
            key="INBOX",
            translation_key="inbox",
        ),
    ),
    # Hub sensors - Energy counter (system variables)
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="svEnergyCounter",
        description=HmSensorEntityDescription(
            key="ENERGY_COUNTER",
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            translation_key="energy_counter_total",
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="svEnergyCounterFeedIn",
        description=HmSensorEntityDescription(
            key="ENERGY_COUNTER_FEED_IN",
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            translation_key="energy_counter_feed_in_total",
        ),
    ),
    # Hub sensors - Rain counter (system variables)
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="svHmIPRainCounter",
        description=HmSensorEntityDescription(
            key="RAIN_COUNTER",
            native_unit_of_measurement=UnitOfLength.MILLIMETERS,
            state_class=SensorStateClass.TOTAL_INCREASING,
            translation_key="rain_counter_total",
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="svHmIPRainCounterToday",
        description=HmSensorEntityDescription(
            key="RAIN_COUNTER_TODAY",
            native_unit_of_measurement=UnitOfLength.MILLIMETERS,
            state_class=SensorStateClass.TOTAL_INCREASING,
            translation_key="rain_counter_today",
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="svHmIPRainCounterYesterday",
        description=HmSensorEntityDescription(
            key="RAIN_COUNTER_YESTERDAY",
            native_unit_of_measurement=UnitOfLength.MILLIMETERS,
            state_class=SensorStateClass.TOTAL_INCREASING,
            translation_key="rain_counter_yesterday",
        ),
    ),
    # Hub sensors - Sunshine counter (system variables)
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="svHmIPSunshineCounter",
        description=HmSensorEntityDescription(
            key="SUNSHINE_COUNTER",
            device_class=SensorDeviceClass.DURATION,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            state_class=SensorStateClass.TOTAL_INCREASING,
            translation_key="sunshine_counter_total",
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="svHmIPSunshineCounterToday",
        description=HmSensorEntityDescription(
            key="SUNSHINE_COUNTER_TODAY",
            device_class=SensorDeviceClass.DURATION,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            state_class=SensorStateClass.TOTAL_INCREASING,
            translation_key="sunshine_counter_today",
        ),
    ),
    EntityDescriptionRule(
        category=DataPointCategory.HUB_SENSOR,
        var_name_contains="svHmIPSunshineCounterYesterday",
        description=HmSensorEntityDescription(
            key="SUNSHINE_COUNTER_YESTERDAY",
            device_class=SensorDeviceClass.DURATION,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            state_class=SensorStateClass.TOTAL_INCREASING,
            translation_key="sunshine_counter_yesterday",
        ),
    ),
]
