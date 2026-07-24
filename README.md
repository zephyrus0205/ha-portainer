# Portainer

Production-oriented Home Assistant integration for Portainer CE multi-endpoint deployments.

## Installation

Install `custom_components/portainer` through HACS as a custom repository, then add Portainer from Settings → Devices & services. Configure the Portainer URL and an `X-API-Key`.

## Current features

- Config Flow and Options Flow
- One DataUpdateCoordinator and Runtime Data
- Automatic endpoint discovery on coordinator refresh
- Cluster and endpoint sensors
- Endpoint online binary sensors
- Manual refresh button
- Diagnostics and English/Korean translations

## Roadmap

Container controls, resource metrics, automation events, stack support, and a Lovelace card are planned for subsequent releases.
