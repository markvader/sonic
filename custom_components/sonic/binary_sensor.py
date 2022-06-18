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

NAME_AUTO_SHUT_OFF_ENABLED = "Auto Shut Off Enabled"

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
        entities.append(SonicAutoShutOffEnabledSensor(device))
    async_add_entities(entities)


class SonicAutoShutOffEnabledSensor(SonicEntity, BinarySensorEntity):
    """Binary sensor that reports if the auto shut off feature is enabled."""

    _attr_device_class = BinarySensorDeviceClass

    def __init__(self, device):
        """Initialize the pending alerts binary sensor."""
        super().__init__("auto_shut_off_enabled", NAME_AUTO_SHUT_OFF_ENABLED, device)

    @property
    def is_on(self):
        """Return true if the auto shut off feature is enabled."""
        return self._device.auto_shut_off_enabled
