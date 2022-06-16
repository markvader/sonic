"""Config flow for Sonic Integration."""
from herolabsapi import Client, InvalidCredentialsError
import voluptuous as vol

from homeassistant import config_entries, core, exceptions
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, LOGGER

DATA_SCHEMA = vol.Schema({vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str})


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """

    session = async_get_clientsession(hass)
    try:
        api = await Client.async_login(
            data[CONF_USERNAME], data[CONF_PASSWORD], session=session
        )
    except InvalidCredentialsError as request_error:
        LOGGER.error("Error connecting to the Sonic API: %s", request_error)
        raise CannotConnect from request_error

    # Use the verified session to discover the first sonic device's name
    sonic_data = await api.sonic.async_get_all_sonic_details()
    first_sonic_id = sonic_data["data"][0]["id"]
    sonic_info = await api.sonic.async_get_sonic_details(first_sonic_id)
    return {"title": sonic_info["name"]}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sonic."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidHost:
                errors["host"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidHost(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""
