"""Asynchronous Portainer API client."""
from __future__ import annotations
from collections.abc import Iterable
from typing import Any
import aiohttp
class PortainerApiError(Exception):
    """Portainer request failed."""
class PortainerApi:
    """Client for the Portainer REST API."""
    def __init__(self, session: aiohttp.ClientSession, base_url: str, api_key: str) -> None:
        self._session = session
        self.base_url = base_url.rstrip("/")
        self._headers = {"X-API-Key": api_key, "Accept": "application/json"}
    async def async_get(self, path: str, **params: str | int | float) -> Any:
        try:
            async with self._session.get(f"{self.base_url}{path}", headers=self._headers, params=params, timeout=15) as response:
                if response.status >= 400:
                    raise PortainerApiError(f"HTTP {response.status}")
                return await response.json()
        except (aiohttp.ClientError, TimeoutError, ValueError) as err:
            raise PortainerApiError(str(err)) from err
    async def async_status(self): return await self.async_get("/api/status")
    async def async_endpoints(self):
        result = await self.async_get("/api/endpoints")
        return list(result) if isinstance(result, Iterable) else []
    async def async_docker_info(self, endpoint_id: int): return await self.async_get(f"/api/endpoints/{endpoint_id}/docker/info")
    async def async_containers(self, endpoint_id: int):
        result = await self.async_get(f"/api/endpoints/{endpoint_id}/docker/containers/json", all="true")
        return list(result) if isinstance(result, Iterable) else []
    async def async_disk_usage(self, endpoint_id: int): return await self.async_get(f"/api/endpoints/{endpoint_id}/docker/system/df")
