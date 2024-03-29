"""Switch representing the Sonic shutoff valve by Hero Labs integration."""
from __future__ import annotations

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
                PressureTestsEnabled(property),
                CloudDisconnectionAlert(property),
                LowBatteryLevelAlert(property),
                DeviceHandleMovedAlert(property),
                HealthCheckFailedAlert(property),
                PressureTestFailedAlert(property),
                PressureTestSkippedAlert(property),
                RadioDisconnectionAlert(property),
                LegionellaCheckAlert(property),
                LowWaterTemperatureAlert(property),
            ]
        )

    async_add_entities(entities)


class SonicSwitch(SonicEntity, SwitchEntity):
    """Switch class for the Sonic valve."""

    def __init__(self, device: SonicDeviceDataUpdateCoordinator) -> None:
        """Initialize the Sonic switch."""
        super().__init__("shutoff_valve", "Sonic Valve Switch", device)
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


class AutoShutOffSwitch(PropertyEntity, SwitchEntity):
    """Switch class for the Property AutoShutOff."""
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device: PropertyDataUpdateCoordinator) -> None:
        """Initialize the Property AutoShutOff switch."""
        super().__init__("auto_shutoff_switch", "Automatic Shutoff Setting", device)
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
        await self._device.api_client.property.async_update_property_settings(self._device.id, {'auto_shut_off': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Close the valve."""
        await self._device.api_client.property.async_update_property_settings(self._device.id, {'auto_shut_off': False})
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
        super().__init__("pressure_tests_enabled", "Pressure Tests Setting", device)
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
        await self._device.api_client.property.async_update_property_settings(self._device.id,
                                                                              {'pressure_tests_enabled': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the Pressure Tests Enabled Function"""
        await self._device.api_client.property.async_update_property_settings(self._device.id,
                                                                              {'pressure_tests_enabled': False})
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


class CloudDisconnectionAlert(PropertyEntity, SwitchEntity):
    """Switch class for the Property CloudDisconnection Alert."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device: PropertyDataUpdateCoordinator) -> None:
        """Initialize the Property CloudDisconnection Alert switch."""
        super().__init__("cloud_disconnection_alert", "Alerts - Cloud Disconnection", device)
        self._state = self._device.property_cloud_disconnection == True

    @property
    def is_on(self) -> bool:
        """Return True if the Alert is enabled."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the switch."""
        if self.is_on:
            return "mdi:bell"
        return "mdi:bell-off"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'cloud_disconnection': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'cloud_disconnection': False})
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest switch state and update the state machine."""
        self._state = self._device.property_cloud_disconnection == True
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))


class LowBatteryLevelAlert(PropertyEntity, SwitchEntity):
    """Switch class for the Property low battery level Alert."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device: PropertyDataUpdateCoordinator) -> None:
        """Initialize the Property low_battery_level Alert switch."""
        super().__init__("low_battery_level_alert", "Alerts - Low Battery Level", device)
        self._state = self._device.property_low_battery_level == True

    @property
    def is_on(self) -> bool:
        """Return True if the Alert is enabled."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the switch."""
        if self.is_on:
            return "mdi:bell"
        return "mdi:bell-off"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'low_battery_level': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'low_battery_level': False})
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest switch state and update the state machine."""
        self._state = self._device.property_low_battery_level == True
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))


class LegionellaCheckAlert(PropertyEntity, SwitchEntity):
    """Switch class for the Property Legionella Check Alert."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device: PropertyDataUpdateCoordinator) -> None:
        """Initialize the Property legionella_check Alert switch."""
        super().__init__("legionella_check_alert", "Alerts - Legionella Check", device)
        self._state = self._device.property_legionella_check == True

    @property
    def is_on(self) -> bool:
        """Return True if the Alert is enabled."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the switch."""
        if self.is_on:
            return "mdi:bell"
        return "mdi:bell-off"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'legionella_risk': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'legionella_risk': False})
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest switch state and update the state machine."""
        self._state = self._device.property_legionella_check == True
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))


class LowWaterTemperatureAlert(PropertyEntity, SwitchEntity):
    """Switch class for the Property Low Water Temperature Alert."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device: PropertyDataUpdateCoordinator) -> None:
        """Initialize the Property Low Water Temperature Alert switch."""
        super().__init__("low_water_temperature_alert", "Alerts - Low Water Temperature", device)
        self._state = self._device.property_low_water_temperature_check == True

    @property
    def is_on(self) -> bool:
        """Return True if the Alert is enabled."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the switch."""
        if self.is_on:
            return "mdi:bell"
        return "mdi:bell-off"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'low_water_temperature': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'low_water_temperature': False})
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest switch state and update the state machine."""
        self._state = self._device.property_low_water_temperature_check == True
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))


class DeviceHandleMovedAlert(PropertyEntity, SwitchEntity):
    """Switch class for the Device Handle Moved Alert."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device: PropertyDataUpdateCoordinator) -> None:
        """Initialize the Property Device Handle Moved Alert switch."""
        super().__init__("device_handle_moved_alert", "Alerts - Valve Position", device)
        self._state = self._device.property_device_handle_moved == True

    @property
    def is_on(self) -> bool:
        """Return True if the Alert is enabled."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the switch."""
        if self.is_on:
            return "mdi:bell"
        return "mdi:bell-off"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'device_handle_moved': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'device_handle_moved': False})
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest switch state and update the state machine."""
        self._state = self._device.property_device_handle_moved == True
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))


class HealthCheckFailedAlert(PropertyEntity, SwitchEntity):
    """Switch class for the Health Check Failed Alert."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device: PropertyDataUpdateCoordinator) -> None:
        """Initialize the Property Health Check Failed Alert switch."""
        super().__init__("health_check_failed_alert", "Alerts - Health Check Failed", device)
        self._state = self._device.property_health_check_failed == True

    @property
    def is_on(self) -> bool:
        """Return True if the Alert is enabled."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the switch."""
        if self.is_on:
            return "mdi:bell"
        return "mdi:bell-off"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'health_check_failed': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'health_check_failed': False})
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest switch state and update the state machine."""
        self._state = self._device.property_health_check_failed == True
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))


class PressureTestFailedAlert(PropertyEntity, SwitchEntity):
    """Switch class for the Pressure Test Failed Alert."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device: PropertyDataUpdateCoordinator) -> None:
        """Initialize the Property Pressure Test Failed Alert switch."""
        super().__init__("pressure_test_failed_alert", "Alerts - Pressure Test Failed", device)
        self._state = self._device.property_pressure_test_failed == True

    @property
    def is_on(self) -> bool:
        """Return True if the Alert is enabled."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the switch."""
        if self.is_on:
            return "mdi:bell"
        return "mdi:bell-off"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'pressure_test_failed': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'pressure_test_failed': False})
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest switch state and update the state machine."""
        self._state = self._device.property_pressure_test_failed == True
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))


class PressureTestSkippedAlert(PropertyEntity, SwitchEntity):
    """Switch class for the Pressure Test Skipped Alert."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device: PropertyDataUpdateCoordinator) -> None:
        """Initialize the Property Pressure Test Skipped Alert switch."""
        super().__init__("pressure_test_skipped_alert", "Alerts - Pressure Test Skipped", device)
        self._state = self._device.property_pressure_test_skipped == True

    @property
    def is_on(self) -> bool:
        """Return True if the Alert is enabled."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the switch."""
        if self.is_on:
            return "mdi:bell"
        return "mdi:bell-off"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'pressure_test_skipped': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'pressure_test_skipped': False})
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest switch state and update the state machine."""
        self._state = self._device.property_pressure_test_skipped == True
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))


class RadioDisconnectionAlert(PropertyEntity, SwitchEntity):
    """Switch class for the Radio Disconnection Alert."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device: PropertyDataUpdateCoordinator) -> None:
        """Initialize the Property Radio Disconnection Alert switch."""
        super().__init__("radio_disconnection_alert", "Alerts - Radio Disconnection", device)
        self._state = self._device.property_radio_disconnection == True

    @property
    def is_on(self) -> bool:
        """Return True if the Alert is enabled."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the switch."""
        if self.is_on:
            return "mdi:bell"
        return "mdi:bell-off"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'radio_disconnection': True})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the Alert"""
        await self._device.api_client.property.async_update_property_notifications(self._device.id,
                                                                                   {'radio_disconnection': False})
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest switch state and update the state machine."""
        self._state = self._device.property_radio_disconnection == True
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))
