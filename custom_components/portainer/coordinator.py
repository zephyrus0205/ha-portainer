"""Portainer data coordinator."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import timedelta
import logging
from typing import Any
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import PortainerApi, PortainerApiError
from .const import DEFAULT_INFO_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN
_LOGGER = logging.getLogger(__name__)
@dataclass(slots=True)
class RuntimeData:
    api: PortainerApi
    coordinator: PortainerCoordinator
class PortainerCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch all API data; entities only consume this cache."""
    def __init__(self, hass: HomeAssistant, api: PortainerApi, entry: ConfigEntry) -> None:
        self.api, self.entry = api, entry
        self._info: dict[int, tuple[float, dict[str, Any]]] = {}
        super().__init__(hass, logger=_LOGGER, name=DOMAIN, update_interval=timedelta(seconds=entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)))
    async def _async_update_data(self) -> dict[str, Any]:
        try:
            endpoints = await self.api.async_endpoints(); data = {"endpoints": {}}
            ids = set()
            for endpoint in endpoints:
                endpoint_id = int(endpoint["Id"]); ids.add(endpoint_id)
                cached = self._info.get(endpoint_id)
                endpoint_data = {"endpoint": endpoint, "info": cached[1] if cached else {}, "containers": [], "online": True}
                try:
                    if cached is None or self.hass.loop.time() - cached[0] >= DEFAULT_INFO_INTERVAL:
                        cached = (self.hass.loop.time(), await self.api.async_docker_info(endpoint_id))
                        self._info[endpoint_id] = cached
                    endpoint_data["info"] = cached[1]
                    endpoint_data["containers"] = await self.api.async_containers(endpoint_id)
                except PortainerApiError as err:
                    endpoint_data["online"] = False
                    _LOGGER.warning("Endpoint %s is unavailable: %s", endpoint_id, err)
                data["endpoints"][endpoint_id] = endpoint_data
            self._info = {key: value for key, value in self._info.items() if key in ids}
            data["status"] = await self.api.async_status()
            return data
        except PortainerApiError as err:
            raise UpdateFailed(str(err)) from err
