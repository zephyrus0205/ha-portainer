"""Portainer refresh and container control buttons."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import PortainerApiError
from .entity import PortainerEntity


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up refresh and container control buttons."""
    coordinator = entry.runtime_data.coordinator
    entities: list[ButtonEntity] = [RefreshButton(coordinator, entry.entry_id)]
    for endpoint_id, endpoint_data in coordinator.data["endpoints"].items():
        for container in endpoint_data["containers"]:
            container_id = str(container["Id"])
            container_name = str(container.get("Names", [container_id])[0]).lstrip("/")
            for action in ("start", "stop", "restart"):
                entities.append(ContainerButton(coordinator, entry.entry_id, endpoint_id, container_id, container_name, action))
    async_add_entities(entities)


class RefreshButton(PortainerEntity, ButtonEntity):
    """Refresh Portainer data."""
    _attr_name = "Refresh"

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_refresh"

    async def async_press(self) -> None:
        await self.coordinator.async_request_refresh()


class ContainerButton(PortainerEntity, ButtonEntity):
    """Start, stop, or restart one Docker container."""

    def __init__(self, coordinator, entry_id, endpoint_id, container_id, container_name, action):
        super().__init__(coordinator, entry_id, endpoint_id)
        self._container_id = container_id
        self._action = action
        self._attr_name = f"{container_name} {action.title()}"
        self._attr_unique_id = f"{entry_id}_{endpoint_id}_{container_id}_{action}"

    async def async_press(self) -> None:
        try:
            await self.coordinator.async_container_action(self.endpoint_id, self._container_id, self._action)
        except PortainerApiError as err:
            raise HomeAssistantError(f"Unable to {self._action} container: {err}") from err
