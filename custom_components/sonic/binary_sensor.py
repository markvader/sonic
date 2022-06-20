"""Support for Sonic Water Valve binary sensors."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN as SONIC_DOMAIN
from .device import SonicDeviceDataUpdateCoordinator
from .entity import SonicEntity

NAME_AUTO_SHUT_OFF_ENABLED = "Auto Shut Off Enabled Status"

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Sonic sensors from config entry."""
    devices: list[SonicDeviceDataUpdateCoordinator] = hass.data[SONIC_DOMAIN][
        config_entry.entry_id
    ]["devices"]
    entities: list[BinarySensorEntity] = []
    for device in devices:
#        entities.append(SonicOpenIncidentsBinarySensor(device))
        entities.append(SonicAutoShutOffEnabledSensor(device))
    async_add_entities(entities)


#class SonicOpenIncidentsBinarySensor(SonicEntity, BinarySensorEntity):
#    """Binary sensor that reports on if there are any open incident reports."""
#
#    _attr_device_class = BinarySensorDeviceClass.PROBLEM
#
#    def __init__(self, device):
#        """Initialize the open incidents binary sensor."""
#        super().__init__("open_incidents", "Open Alert Reports", device)
#
#    @property
#    def is_on(self):
#        """Return true if the Sonic device has open incidents."""
#        return self._device.has_incidents
#
#    @property
#    def extra_state_attributes(self):
#        """Return the state attributes."""
#        if not self._device.has_alerts:
#            return {}
#        return {
#            "low": self._device.low_severity_alerts_count,
#            "high": self._device.high_severity_alerts_count,
#        }


class SonicAutoShutOffEnabledSensor(SonicEntity, BinarySensorEntity):
    """Binary sensor that reports if the auto shut off feature is enabled."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING

    def __init__(self, device):
        """Initialize the pending alerts binary sensor."""
        super().__init__("auto_shut_off_enabled", NAME_AUTO_SHUT_OFF_ENABLED, device)

    @property
    def is_on(self):
        """Return true if the auto shut off feature is enabled."""
        return self._device.auto_shut_off_enabled
