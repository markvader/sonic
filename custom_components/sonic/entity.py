"""Base entity class for Sonic & Property entities."""
from __future__ import annotations

from typing import Any

from homeassistant.helpers.entity import DeviceInfo, Entity

from .const import DOMAIN as SONIC_DOMAIN
from .device import SonicDeviceDataUpdateCoordinator
from .property import PropertyDataUpdateCoordinator

class SonicEntity(Entity):
    """A base class for Sonic entities."""

    _attr_force_update = False
    _attr_should_poll = False

    def __init__(
        self,
        entity_type: str,
        name: str,
        device: SonicDeviceDataUpdateCoordinator,
        **kwargs,
    ) -> None:
        """Init Sonic entity."""
        self._attr_name = name
        self._attr_unique_id = f"{device.serial_number}_{entity_type}"

        self._device: SonicDeviceDataUpdateCoordinator = device
        self._state: Any = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return DeviceInfo(
            identifiers={(SONIC_DOMAIN, self._device.id)},
            manufacturer=self._device.manufacturer,
            model=self._device.model,
            name=f'Sonic Device: {self._device.device_name}',
        )

    @property
    def available(self) -> bool:
        """Return True if device is available."""
        return self._device.available

    async def async_update(self):
        """Update Sonic entity."""
        await self._device.async_request_refresh()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_write_ha_state))


class PropertyEntity(Entity):
    """A base class for Property entities."""

    _attr_force_update = False
    _attr_should_poll = False

    def __init__(
        self,
        entity_type: str,
        name: str,
        property: PropertyDataUpdateCoordinator,
        **kwargs,
    ) -> None:
        """Init Property entity."""
        self._attr_name = name
        self._attr_unique_id = f"{property.id}_{entity_type}"

        self._device: PropertyDataUpdateCoordinator = property
        self._state: Any = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return DeviceInfo(
            identifiers={(SONIC_DOMAIN, self._device.id)},
            manufacturer="Hero Labs",
            model="Property",
            name=f'Sonic Property Settings: {self._device.property_name}',
        )

    @property
    def available(self) -> bool:
        """Return True if property is available."""
        return self._device.id != None

    async def async_update(self):
        """Update Property entity."""
        await self._property.async_request_refresh()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_write_ha_state))
