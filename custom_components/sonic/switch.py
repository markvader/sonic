"""Switch representing the Sonic shutoff valve by Hero Labs integration."""
from __future__ import annotations

import voluptuous as vol
from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN as SONIC_DOMAIN
from .device import SonicDeviceDataUpdateCoordinator
from .property import PropertyDataUpdateCoordinator
from .entity import SonicEntity, PropertyEntity

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
        entities.extend(
            [
                SonicSwitch(device),
            ]
        )

    properties: list[PropertyDataUpdateCoordinator] = hass.data[SONIC_DOMAIN][config_entry.entry_id]["properties"]
    for property in properties:
        entities.extend(
            [
                AutoShutOffSwitch(property),
                PressureTestsEnabled(property)
            ]
        )

    async_add_entities(entities)


class SonicSwitch(SonicEntity, SwitchEntity):
    """Switch class for the Sonic valve."""

    def __init__(self, device: SonicDeviceDataUpdateCoordinator) -> None:
        """Initialize the Sonic switch."""
        super().__init__("shutoff_valve", "Shutoff Valve", device)
        self._state = self._device.last_known_valve_state is "open"

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
        self._state = self._device.last_known_valve_state is "open"
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))


class AutoShutOffSwitch(PropertyEntity, SwitchEntity):
    """Switch class for the Property AutoShutOff."""
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device: PropertyDataUpdateCoordinator) -> None:
        """Initialize the Property AutoShutOff switch."""
        super().__init__("auto_shutoff_switch", "Auto Shutoff Function", device)
        self._state = self._device.property_auto_shut_off == True

    @property
    def is_on(self) -> bool:
        """Return True if the AutoShutoff is enabled."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the switch."""
        if self.is_on:
            return "mdi:auto-fix"
        return "mdi:exclamation-thick"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the AutoShutOff Function"""
        await self._device.api_client.property.async_update_property_settings(self._device.id, json={'auto_shut_off': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Close the valve."""
        await self._device.api_client.property.async_update_property_settings(self._device.id, json={'auto_shut_off': False})
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest switch state and update the state machine."""
        self._state = self._device.property_auto_shut_off == True
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))


class PressureTestsEnabled(PropertyEntity, SwitchEntity):
    """Switch class for the Property pressure_tests_enabled."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device: PropertyDataUpdateCoordinator) -> None:
        """Initialize the Property Pressure Tests Enabled switch."""
        super().__init__("pressure_tests_enabled", "Pressure Tests Function", device)
        self._state = self._device.property_pressure_tests_enabled == True

    @property
    def is_on(self) -> bool:
        """Return True if the Pressure Tests Enabled is enabled."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the switch."""
        if self.is_on:
            return "mdi:auto-fix"
        return "mdi:exclamation-thick"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the Pressure Tests Enabled Function"""
        await self._device.api_client.property.async_update_property_settings(self._device.id, json={'pressure_tests_enabled': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the Pressure Tests Enabled Function"""
        await self._device.api_client.property.async_update_property_settings(self._device.id, json={'pressure_tests_enabled': False})
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest switch state and update the state machine."""
        self._state = self._device.property_pressure_tests_enabled == True
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))
