"""Portainer endpoint status sensors."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .entity import PortainerEntity
async def async_setup_entry(hass,entry:ConfigEntry,async_add_entities:AddEntitiesCallback): async_add_entities([OnlineSensor(entry.runtime_data.coordinator,entry.entry_id,eid) for eid in entry.runtime_data.coordinator.data["endpoints"]])
class OnlineSensor(PortainerEntity,BinarySensorEntity):
    _attr_name="Online"
    def __init__(self,c,eid,endpoint_id): super().__init__(c,eid,endpoint_id); self._attr_unique_id=f"{eid}_{endpoint_id}_online"
    @property
    def is_on(self): return self.coordinator.data["endpoints"].get(self.endpoint_id, {}).get("online", False)
