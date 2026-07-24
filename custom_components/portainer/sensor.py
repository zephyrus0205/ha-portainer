"""Portainer sensors."""
from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .entity import PortainerEntity

def _counts(data):
    containers=[c for e in data["endpoints"].values() for c in e["containers"]]
    return sum(c.get("State")=="running" for c in containers),sum(c.get("State")!="running" for c in containers),len(containers)
async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry,async_add_entities:AddEntitiesCallback):
    c=entry.runtime_data.coordinator; entities=[ClusterSensor(c,entry.entry_id,k) for k in ("running","stopped","total")]
    entities += [EndpointSensor(c,entry.entry_id,eid,k) for eid in c.data["endpoints"] for k in ("running","total","images","volumes")]
    async_add_entities(entities)
class ClusterSensor(PortainerEntity,SensorEntity):
    def __init__(self,c,eid,key): super().__init__(c,eid); self.key=key; self._attr_unique_id=f"{eid}_cluster_{key}"; self._attr_name=key.title()
    @property
    def native_value(self): return _counts(self.coordinator.data)[{"running":0,"stopped":1,"total":2}[self.key]]
class EndpointSensor(PortainerEntity,SensorEntity):
    def __init__(self,c,eid,endpoint_id,key): super().__init__(c,eid,endpoint_id); self.key=key; self._attr_unique_id=f"{eid}_{endpoint_id}_{key}"; self._attr_name=key.title()
    @property
    def native_value(self):
        d=self.coordinator.data["endpoints"].get(self.endpoint_id); 
        if not d:return None
        if self.key in ("running","total"): return _counts({"endpoints":{0:d}})[{"running":0,"total":2}[self.key]]
        return d["info"].get("Images",0) if self.key=="images" else d["info"].get("Volumes",0)
