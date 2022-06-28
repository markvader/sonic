"""The Sonic Water Shut-off Valve integration."""
from __future__ import annotations
from datetime import datetime
import pytz

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PRESSURE_BAR,
    TEMP_CELSIUS,
    VOLUME_LITERS,
    TIME_MINUTES,
    VOLUME_LITERS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN as SONIC_DOMAIN, LOGGER
from .device import SonicDeviceDataUpdateCoordinator
from .property import PropertyDataUpdateCoordinator
from .entity import SonicEntity, PropertyEntity

WATER_ICON = "mdi:water"
GAUGE_ICON = "mdi:gauge"
BATTERY_ICON = "mdi:battery"
TIMER_ICON = "mdi:timer"
VOLUME_ICON = "mdi:cup-water"
VALVE_ICON = "mdi:valve"
NAME_FLOW_RATE = "Water Flow Rate"
NAME_WATER_TEMPERATURE = "Water Temperature"
NAME_WATER_PRESSURE = "Water Pressure"
NAME_BATTERY = "Battery"
NAME_VALVE_STATE = "Current Valve State"
NAME_DEVICE_STATUS = "Sonic Status Message"
NAME_AUTO_SHUT_OFF_TIME_LIMIT = "Auto Shut Off Time Limit"
NAME_AUTO_SHUT_OFF_VOLUME_LIMIT = "Auto Shut Off Volume Limit"
NAME_LONG_FLOW_NOTIFICATION_DELAY = "Long Flow Notification Time Delay"
NAME_HIGH_VOLUME_THRESHOLD_LITRES = "High Volume Notification Threshold"
NAME_TELEMETRYTIME = "Telemetry Data Timestamp"

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Sonic sensors from config entry."""
    devices: list[SonicDeviceDataUpdateCoordinator] = hass.data[SONIC_DOMAIN][
        config_entry.entry_id
    ]["devices"]
    entities = []
    for device in devices:
        entities.extend(
            [
                SonicCurrentFlowRateSensor(device),
                SonicTemperatureSensor(device),
                SonicPressureSensor(device),
                SonicBatterySensor(device),
                SonicTelemetryTime(device),
                SonicValveStateSensor(device),
                SonicDeviceStatusSensor(device),
                SonicAutoShutOffTimeLimitSensor(device),
                SonicAutoShutOffVolumeLimitSensor(device),
            ]
        )
    """Set up the Property sensors from config entry."""
    properties: list[PropertyDataUpdateCoordinator] = hass.data[SONIC_DOMAIN][
        config_entry.entry_id
    ]["properties"]
    for property in properties:
        entities.extend(
            [
                PropertyLongFlowNotificationDelay(property),
                PropertyHighVolumeNotificationThresholdLitres(property),
            ]
        )
    async_add_entities(entities)


class SonicCurrentFlowRateSensor(SonicEntity, SensorEntity):
    """Monitors the current water flow rate."""

    _attr_icon = GAUGE_ICON
    _attr_native_unit_of_measurement = "litres per min"
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, device):
        """Initialize the flow rate sensor."""
        super().__init__("current_flow_rate", NAME_FLOW_RATE, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current flow rate in Litre per minute."""
        if self._device.current_flow_rate is None:
            return None
        return round(((self._device.current_flow_rate)/1000), 1)


class SonicTemperatureSensor(SonicEntity, SensorEntity):
    """Monitors the water temperature."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, device):
        """Initialize the temperature sensor."""
        super().__init__("temperature", NAME_WATER_TEMPERATURE, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current temperature."""
        if self._device.temperature is None:
            return None
        return round(self._device.temperature, 1)


class SonicPressureSensor(SonicEntity, SensorEntity):
    """Monitors the water pressure."""

    _attr_device_class = SensorDeviceClass.PRESSURE
    _attr_native_unit_of_measurement = PRESSURE_BAR
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, device):
        """Initialize the water pressure sensor."""
        super().__init__("water_pressure", NAME_WATER_PRESSURE, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current water pressure in bar."""
        if self._device.current_mbar is None:
            return None
        return round(((self._device.current_mbar)/1000), 1)


class SonicBatterySensor(SonicEntity, SensorEntity):
    """Monitors the battery state for battery-powered devices or returns external_power_supply if externally powered."""

    _attr_icon = BATTERY_ICON
    _attr_native_unit_of_measurement = "battery"
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, device):
        """Initialize the battery sensor."""
        super().__init__("battery", NAME_BATTERY, device)
        self._state: str = None

    @property
    def native_value(self) -> str | None:
        """Return the current battery state."""
        return self._device.battery_state


class SonicTelemetryTime(SonicEntity, SensorEntity):
    """Returns time that the telemetry data was captured at by sonic."""

    _attr_icon = TIMER_ICON
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, device):
        """Initialize the telemetry time sensor."""
        super().__init__("telemetry_time", NAME_TELEMETRYTIME, device)
        self._state: str = None

    @property
    def native_value(self) -> str | None:
        """Return the current telemetry time state."""
        telemetry_timestamp = self._device.last_heard_from_time
        # telemetry_timezone = self._device.property_timezone
        timezone = pytz.timezone("Europe/London")
        telemetry_datetime = datetime.fromtimestamp(telemetry_timestamp, timezone)
        return telemetry_datetime


class SonicValveStateSensor(SonicEntity, SensorEntity):
    """Return the current valve state
       Options are: 'open, closed, opening, closing, faulty, pressure_test, requested_open, requested_closed' """

    _attr_icon = VALVE_ICON

    def __init__(self, device):
        """Initialize the current valve state sensor."""
        super().__init__("valve_state", NAME_VALVE_STATE, device)
        self._state: str = None

    @property
    def native_value(self) -> str | None:
        """Return the current valve state state."""
        if not self._device.last_heard_from_time:
            return None
        return self._device.last_known_valve_state


class SonicDeviceStatusSensor(SonicEntity, SensorEntity):
    """Return any sonic status message"""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, device):
        """Initialize the device status sensor."""
        super().__init__("device_status", NAME_DEVICE_STATUS, device)
        self._state: str = None

    @property
    def native_value(self) -> str | None:
        """Return the device status state."""
        if not self._device.sonic_status:
            return None
        return self._device.sonic_status


class SonicAutoShutOffTimeLimitSensor(SonicEntity, SensorEntity):
    """Return the auto_shut_off_time_limit state"""

    _attr_icon = TIMER_ICON
    _attr_native_unit_of_measurement = TIME_MINUTES
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, device):
        """Initialize the auto_shut_off_time_limit sensor."""
        super().__init__("auto_shut_off_time_limit", NAME_AUTO_SHUT_OFF_TIME_LIMIT, device)
        self._state: int = None

    @property
    def native_value(self) -> int | None:
        """Return the auto_shut_off_time_limit state in minutes."""
        return round((self._device.auto_shut_off_time_limit)/60)


class SonicAutoShutOffVolumeLimitSensor(SonicEntity, SensorEntity):
    """Return the auto_shut_off_volume_limit state"""

    _attr_icon = VOLUME_ICON
    _attr_native_unit_of_measurement = VOLUME_LITERS
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, device):
        """Initialize the auto_shut_off_volume_limit sensor."""
        super().__init__("auto_shut_off_volume_limit", NAME_AUTO_SHUT_OFF_VOLUME_LIMIT, device)
        self._state: int = None

    @property
    def native_value(self) -> int | None:
        """Return the auto_shut_off_volume_limit state."""
        return round((self._device.auto_shut_off_volume_limit)/1000)

class PropertyLongFlowNotificationDelay(PropertyEntity, SensorEntity):
    """Return the long flow notification delay in minutes at property"""

    _attr_icon = TIMER_ICON
    _attr_native_unit_of_measurement = TIME_MINUTES
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, property):
        """Initialize the property_long_flow_notification_delay_mins sensor."""
        super().__init__("property_long_flow_notification_delay_mins", NAME_LONG_FLOW_NOTIFICATION_DELAY, property)
        self._state: int = None

    @property
    def native_value(self) -> int | None:
        """Return the property_long_flow_notification_delay in minutes."""
        return self._device.property_long_flow_notification_delay_mins

class PropertyHighVolumeNotificationThresholdLitres(PropertyEntity, SensorEntity):
    """Return the high_volume_threshold_litres at property"""

    _attr_icon = TIMER_ICON
    _attr_native_unit_of_measurement = VOLUME_LITERS
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, property):
        """Initialize the property_high_volume_threshold_litres sensor."""
        super().__init__("property_high_volume_threshold_litres", NAME_HIGH_VOLUME_THRESHOLD_LITRES, property)
        self._state: int = None

    @property
    def native_value(self) -> int | None:
        """Return the property_high_volume_threshold_litres."""
        return self._device.property_high_volume_threshold_litres
