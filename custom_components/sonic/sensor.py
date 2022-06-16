"""The Sonic Water Shut-off Valve integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PRESSURE_MBAR,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN as SONIC_DOMAIN
from .device import SonicDeviceDataUpdateCoordinator
from .entity import SonicEntity

WATER_ICON = "mdi:water"
GAUGE_ICON = "mdi:gauge"
NAME_FLOW_RATE = "Water Flow Rate"
NAME_WATER_TEMPERATURE = "Water Temperature"
NAME_WATER_PRESSURE = "Water Pressure"
NAME_BATTERY = "Battery"


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
                SonicTemperatureSensor(NAME_WATER_TEMPERATURE, device),
                SonicPressureSensor(device),
                SonicBatterySensor(device),
            ]
        )
    async_add_entities(entities)


class SonicCurrentFlowRateSensor(SonicEntity, SensorEntity):
    """Monitors the current water flow rate."""

    _attr_icon = GAUGE_ICON
    _attr_native_unit_of_measurement = "millilitres per min"
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, device):
        """Initialize the flow rate sensor."""
        super().__init__("current_flow_rate", NAME_FLOW_RATE, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current flow rate."""
        if self._device.current_flow_rate is None:
            return None
        return round(self._device.current_flow_rate, 1)


class SonicTemperatureSensor(SonicEntity, SensorEntity):
    """Monitors the water temperature."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, name, device):
        """Initialize the temperature sensor."""
        super().__init__("temperature", name, device)
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
    _attr_native_unit_of_measurement = PRESSURE_MBAR
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, device):
        """Initialize the water pressure sensor."""
        super().__init__("water_pressure", NAME_WATER_PRESSURE, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current water pressure."""
        if self._device.current_mbar is None:
            return None
        return round(self._device.current_mbar, 1)


class SonicBatterySensor(SonicEntity, SensorEntity):
    """Monitors the battery state for battery-powered devices or returns external_power_supply if externally powered."""

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
