"""The kostal component."""
import voluptuous as vol


from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import (
    CONF_NAME,
    CONF_HOST,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_MONITORED_CONDITIONS,
    Platform
)
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant

from .const import DEFAULT_NAME, DOMAIN, SENSOR_TYPES

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR, Platform.UPDATE]

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Required(CONF_HOST): cv.string,
                vol.Required(CONF_MONITORED_CONDITIONS): vol.All(
                    cv.ensure_list, [vol.In(list(SENSOR_TYPES))]
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Platform setup, do nothing."""
    if DOMAIN not in config:
        return True

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=dict(config[DOMAIN])
        )
    )
    return True


async def async_setup_entry(hass:  HomeAssistant, entry: ConfigEntry) -> bool:
    """Load the saved entities."""
    coordinator = HassioDataUpdateCoordinator(hass, entry, dev_reg)
    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
