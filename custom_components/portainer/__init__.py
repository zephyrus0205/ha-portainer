"""The Portainer integration."""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .api import PortainerApi, PortainerApiError
from .const import CONF_API_KEY, CONF_BASE_URL, DOMAIN, PLATFORMS
from .coordinator import PortainerCoordinator, RuntimeData
async def async_setup(hass: HomeAssistant, config: dict) -> bool: return True
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = PortainerApi(async_get_clientsession(hass), entry.data[CONF_BASE_URL], entry.data[CONF_API_KEY])
    coordinator = PortainerCoordinator(hass, api, entry)
    try: await coordinator.async_config_entry_first_refresh()
    except (PortainerApiError, UpdateFailed) as err: raise ConfigEntryNotReady from err
    entry.runtime_data = RuntimeData(api, coordinator)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None: await hass.config_entries.async_reload(entry.entry_id)
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool: return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
