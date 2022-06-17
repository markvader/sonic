"""Sonic device object."""
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


class SonicDeviceDataUpdateCoordinator(DataUpdateCoordinator):
    """Sonic device object."""

    def __init__(self, hass: HomeAssistant, api_client: Client, device_id: str) -> None:
        """Initialize the device."""
        self.hass: HomeAssistant = hass
        self.api_client: Client = api_client
        self._sonic_device_id: str = device_id
        self._device_information: dict[str, Any] = {}
        self._telemetry_information: dict[str, Any] = {}
        super().__init__(
            hass,
            LOGGER,
            name=f"{SONIC_DOMAIN}-{device_id}",
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            async with timeout(10):
                await asyncio.gather(
                    *[
                        self._update_device(),
                    ]
                )
        except (RequestError) as error:
            raise UpdateFailed(error) from error

    @property
    def id(self) -> str:
        """Return Sonic device id."""
        return self._sonic_device_id

    @property
    def device_name(self) -> str:
        """Return device name."""
        return self._device_information.get("name", f"{self.model}")

    @property
    def manufacturer(self) -> str:
        """Return manufacturer for device."""
        return "Hero Labs"

    @property
    def serial_number(self) -> str:
        """Return serial number for device."""
        return self._device_information["serial_no"]

    @property
    def model(self) -> str:
        """Return model for device."""
        return "Sonic"

    @property
    def rssi(self) -> float:
        """Return rssi for device."""
        return self._device_information["radio_rssi"]

    @property
    def last_heard_from_time(self) -> str:
        """Return Unix timestamp in seconds when the sonic took measurements
        Will need to do conversion from timestamp to datetime if HomeAssistant doesn't do it automatically"""
        return self._telemetry_information["probed_at"]

    @property
    def available(self) -> bool:
        """Return True if device is available."""
        return (
            self.last_update_success
            and self._device_information["radio_connection"] == "connected"
        )

    @property
    def current_flow_rate(self) -> float:
        """Return current flow rate in ml/min."""
        return self._telemetry_information["water_flow"]

    @property
    def current_mbar(self) -> int:
        """Return the current pressure in mbar."""
        return self._telemetry_information["pressure"]

    @property
    def temperature(self) -> float:
        """Return the current temperature in degrees C."""
        return self._telemetry_information["water_temp"]

    @property
    def battery_state(self) -> str:
        """Return the battery level "high","mid","low" or returns "external_power_supply" """
        return self._device_information["battery"]

    @property
    def auto_shut_off_enabled(self) -> bool:
        """Return the auto shut off enabled boolean"""
        return self._device_information["auto_shut_off_enabled"]

    @property
    def auto_shut_off_time_limit(self) -> int:
        """Return the Sonic offline auto shut off water usage time limit in seconds[0;integer::max).
        When set to 0 usage time check is not performed."""
        return self._device_information["auto_shut_off_time_limit"]

    @property
    def auto_shut_off_volume_limit(self) -> int:
        """Return the Sonic offline auto shut off used water volume limit in millilitres [0;integer::max).
        When set to 0 volume used check is not performed."""
        return self._device_information["auto_shut_off_volume_limit"]

    @property
    def signal_id(self) -> str:
        """Return the associated signal device id
        A Signal device (sometimes called hub) communicates with WiFi and the Sonic device"""
        return self._device_information["signal_id"]

    @property
    def sonic_status(self) -> str:
        """Return any sonic status message"""
        return self._device_information["status"]

    @property
    def last_known_valve_state(self) -> str:
        """Return the current valve state
        Options are: 'open, closed, opening, closing, faulty, pressure_test, requested_open, requested_closed'"""
        return self._device_information["valve_state"]

    async def _update_device(self, *_) -> None:
        """Update the device information from the API."""
        self._device_information = await self.api_client.sonic.async_get_sonic_details(
            self._sonic_device_id
        )
        self._telemetry_information = (
            await self.api_client.sonic.async_sonic_telemetry_by_id(
                self._sonic_device_id
            )
        )
        LOGGER.debug("Sonic device data: %s", self._device_information)
        LOGGER.debug("Sonic telemetry data: %s", self._telemetry_information)
