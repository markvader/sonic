"""Sonic property object."""
from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import Any

from async_timeout import timeout
from herolabsapi.client import Client
from herolabsapi.errors import RequestError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN as SONIC_DOMAIN, LOGGER


class PropertyDataUpdateCoordinator(DataUpdateCoordinator):
    """Sonic property object."""

    def __init__(self, hass: HomeAssistant, api_client: Client, property_id: str) -> None:
        """Initialize the property."""
        self.hass: HomeAssistant = hass
        self.api_client: Client = api_client
        self._sonic_property_id: str = property_id
        self._property_information: dict[str, Any] = {}
        super().__init__(
            hass,
            LOGGER,
            name=f"{SONIC_DOMAIN}-{property_id}",
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            async with timeout(10):
                await asyncio.gather(
                    *[
                        self._update_property(),
                    ]
                )
        except (RequestError) as error:
            raise UpdateFailed(error) from error

    @property
    def id(self) -> str:
        """Return Sonic property id."""
        return self._sonic_property_id

    @property
    def property_name(self) -> str:
        """Return property name."""
        return self._property_information["name"]

    @property
    def property_active(self) -> bool:
        """Return True if property is active."""
        return self._property_information["active"]

    @property
    def property_auto_shut_off(self) -> bool:
        """Return True if auto shut off is enabled at property."""
        return self._property_settings["auto_shut_off"]

    @property
    def property_pressure_tests_enabled(self) -> bool:
        """Return True if pressure tests are enabled at property."""
        return self._property_settings["pressure_tests_enabled"]

    @property
    def property_pressure_tests_schedule(self) -> str:
        """Returns the time that pressure tests are enabled at property.
        The format is HH:MM:SS in 24h clock"""
        return self._property_settings["pressure_tests_schedule"]

    @property
    def property_timezone(self) -> str:
        """Return the timezone set at property."""
        return self._property_settings["timezone"]

    @property
    def property_cloud_disconnection(self) -> bool:
        """Return True if the cloud disconnection notification is enabled at property."""
        return self._property_notification_settings["cloud_disconnection"]

    @property
    def property_device_handle_moved(self) -> bool:
        """Return True if the device handle moved notification is enabled at property."""
        return self._property_notification_settings["device_handle_moved"]

    @property
    def property_health_check_failed(self) -> bool:
        """Return True if the health check failed notification is enabled at property."""
        return self._property_notification_settings["health_check_failed"]

    @property
    def property_high_volume_threshold_litres(self) -> int:
        """Return the high volume threshold litres at property."""
        return self._property_notification_settings["high_volume_threshold_litres"]

    @property
    def property_long_flow_notification_delay_mins(self) -> int:
        """Return the long flow notification delay in minutes at property."""
        return self._property_notification_settings["long_flow_notification_delay_mins"]

    @property
    def property_low_battery_level(self) -> bool:
        """Return True if the low battery level notification is enabled at property."""
        return self._property_notification_settings["low_battery_level"]

    @property
    def property_pressure_test_failed(self) -> bool:
        """Return True if the pressure test failed notification is enabled at property."""
        return self._property_notification_settings["pressure_test_failed"]

    @property
    def property_pressure_test_skipped(self) -> bool:
        """Return True if the pressure test skipped notification is enabled at property."""
        return self._property_notification_settings["pressure_test_skipped"]

    @property
    def property_radio_disconnection(self) -> bool:
        """Return True if the radio disconnection notification is enabled at property."""
        return self._property_notification_settings["radio_disconnection"]


    async def _update_property(self, *_) -> None:
        """Update the property information from the API."""
        self._property_information = await self.api_client.property.async_get_property_details(
            self._sonic_property_id
        )
        self._property_settings = (
            await self.api_client.property.async_get_property_settings(
                self._sonic_property_id
            )
        )
        self._property_notification_settings = (
            await self.api_client.property.async_get_property_notification_settings(
                self._sonic_property_id
            )
        )
        LOGGER.debug("Sonic property data: %s", self._property_information)
        LOGGER.debug("Sonic property settings: %s", self._property_settings)
        LOGGER.debug("Sonic property notification settings: %s", self._property_notification_settings)
