"""Constants for the Portainer integration."""
from homeassistant.const import Platform
DOMAIN = "portainer"
CONF_API_KEY = "api_key"
CONF_BASE_URL = "base_url"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_INFO_INTERVAL = 300
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.BUTTON]
ATTR_ENDPOINT_ID = "endpoint_id"
ATTR_ENDPOINT_NAME = "endpoint_name"
