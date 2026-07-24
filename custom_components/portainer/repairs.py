"""Repair flows for Portainer."""
from __future__ import annotations
from homeassistant.components.repairs import RepairsFlow
from homeassistant.core import HomeAssistant

class PortainerRepairFlow(RepairsFlow):
    """Explain a Portainer repair issue."""
    async def async_step_init(self, user_input=None):
        return self.async_show_form(step_id="init")

async def async_create_fix_flow(hass: HomeAssistant, issue_id: str, data: dict | None = None) -> RepairsFlow:
    """Create the Portainer repair flow."""
    return PortainerRepairFlow()
