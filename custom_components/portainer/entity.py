"""Base entities for Portainer."""
from __future__ import annotations
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .coordinator import PortainerCoordinator
class PortainerEntity(CoordinatorEntity[PortainerCoordinator]):
    _attr_has_entity_name=True
    def __init__(self,coordinator,entry_id,endpoint_id=None):
        super().__init__(coordinator); self._entry_id=entry_id; self.endpoint_id=endpoint_id
    @property
    def device_info(self):
        if self.endpoint_id is None: return DeviceInfo(identifiers={(DOMAIN,self._entry_id)},name="Portainer Cluster",manufacturer="Portainer")
        endpoint=self.coordinator.data["endpoints"].get(self.endpoint_id,{}).get("endpoint",{})
        return DeviceInfo(identifiers={(DOMAIN,f"endpoint_{self.endpoint_id}")},name=endpoint.get("Name",f"Endpoint {self.endpoint_id}"),manufacturer="Portainer",via_device=(DOMAIN,self._entry_id))
