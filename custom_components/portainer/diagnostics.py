"""Diagnostics for Portainer."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.diagnostics import async_redact_data
TO_REDACT={"api_key","X-API-Key"}
async def async_get_config_entry_diagnostics(hass:HomeAssistant,entry:ConfigEntry):
    data=entry.runtime_data.coordinator.data
    return async_redact_data({"portainer_version":data.get("status",{}).get("Version"),"endpoint_count":len(data.get("endpoints",{})),"endpoints":data.get("endpoints",{}),"connection":entry.runtime_data.coordinator.last_update_success},TO_REDACT)
