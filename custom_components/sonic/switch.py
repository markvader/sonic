"""Switch representing the Sonic shutoff valve by Hero Labs integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN as SONIC_DOMAIN
from .device import SonicDeviceDataUpdateCoordinator
from .entity import SonicEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Sonic switches from config entry."""
    devices: list[SonicDeviceDataUpdateCoordinator] = hass.data[SONIC_DOMAIN][
        config_entry.entry_id
    ]["devices"]
    entities = []
    for device in devices:
        entities.append(SonicSwitch(device))
    async_add_entities(entities)


class SonicSwitch(SonicEntity, SwitchEntity):
    """Switch class for the Sonic valve."""

    def __init__(self, device: SonicDeviceDataUpdateCoordinator) -> None:
        """Initialize the Sonic switch."""
        super().__init__("shutoff_valve", "Shutoff Valve", device)
        self._state = self._device.last_known_valve_state == "open"

    @property
    def is_on(self) -> bool:
        """Return True if the valve is open."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the valve."""
        if self.is_on:
            return "mdi:valve-open"
        return "mdi:valve-closed"

    async def async_turn_on(self, **kwargs) -> None:
        """Open the valve."""
        await self._device.api_client.sonic.async_open_sonic_valve(self._device.id)
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Close the valve."""
        await self._device.api_client.sonic.async_close_sonic_valve(self._device.id)
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest valve state and update the state machine."""
        self._state = self._device.last_known_valve_state == "open"
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))
