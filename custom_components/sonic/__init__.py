"""The Sonic Water Shut-off Valve integration."""
import logging
import asyncio

from herolabsapi import (
    InvalidCredentialsError,
    Client,
    ServiceUnavailableError,
    TooManyRequestsError,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CLIENT, DOMAIN
from .device import SonicDeviceDataUpdateCoordinator
from .property import PropertyDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["switch", "sensor", "binary_sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Sonic Water Shut-off Valve from a config entry."""
    session = async_get_clientsession(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}
    try:
        hass.data[DOMAIN][entry.entry_id][CLIENT] = client = await Client.async_login(
            entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD], session=session
        )
    except InvalidCredentialsError as err:
        raise ConfigEntryNotReady from err

    sonic_data = await client.sonic.async_get_all_sonic_details()

    _LOGGER.debug("Sonic device data information: %s", sonic_data)

    hass.data[DOMAIN][entry.entry_id]["devices"] = devices = [
        SonicDeviceDataUpdateCoordinator(hass, client, device["id"])
        for device in sonic_data["data"]
    ]

    sonic_task = [device.async_refresh() for device in devices]

    property_data = await client.property.async_get_all_property_details()

    _LOGGER.debug("Sonic property data information: %s", property_data)

    hass.data[DOMAIN][entry.entry_id]["properties"] = properties = [
        PropertyDataUpdateCoordinator(hass, client, property["id"])
        for property in property_data["data"]
    ]

    property_task = [property.async_refresh() for property in properties]

    await asyncio.gather(*sonic_task, *property_task)

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
