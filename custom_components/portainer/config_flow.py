"""Config flow for Portainer."""
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .api import PortainerApi, PortainerApiError
from .const import CONF_BASE_URL, DEFAULT_SCAN_INTERVAL, DOMAIN
class PortainerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION=1
    async def async_step_user(self,user_input=None):
        errors={}
        if user_input:
            try: status=await PortainerApi(async_get_clientsession(self.hass),user_input[CONF_BASE_URL],user_input[CONF_API_KEY]).async_status()
            except PortainerApiError: errors["base"]="cannot_connect"
            else:
                await self.async_set_unique_id(user_input[CONF_BASE_URL].rstrip("/")); self._abort_if_unique_id_configured()
                return self.async_create_entry(title=str(status.get("Version","Portainer")),data=user_input)
        schema=vol.Schema({vol.Required(CONF_BASE_URL,default="http://localhost:9000"):str,vol.Required(CONF_API_KEY):str})
        return self.async_show_form(step_id="user",data_schema=schema,errors=errors)
    @staticmethod
    def async_get_options_flow(config_entry): return PortainerOptionsFlow(config_entry)
class PortainerOptionsFlow(config_entries.OptionsFlow):
    def __init__(self,config_entry): self.config_entry=config_entry
    async def async_step_init(self,user_input=None):
        if user_input is not None: return self.async_create_entry(title="",data=user_input)
        return self.async_show_form(step_id="init",data_schema=vol.Schema({vol.Required("scan_interval",default=self.config_entry.options.get("scan_interval",DEFAULT_SCAN_INTERVAL)):vol.All(vol.Coerce(int),vol.Range(min=10,max=3600))}))
