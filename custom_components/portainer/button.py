"""Portainer buttons."""
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .entity import PortainerEntity
async def async_setup_entry(hass,entry:ConfigEntry,async_add_entities:AddEntitiesCallback): async_add_entities([RefreshButton(entry.runtime_data.coordinator,entry.entry_id)])
class RefreshButton(PortainerEntity,ButtonEntity):
    _attr_name="Refresh"
    def __init__(self,c,eid): super().__init__(c,eid); self._attr_unique_id=f"{eid}_refresh"
    async def async_press(self): await self.coordinator.async_request_refresh()
