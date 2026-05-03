import json
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.components import mqtt
from homeassistant.helpers.entity import DeviceInfo
from .const import CONF_DEVICE_ID, DOMAIN, TOPIC_COMMAND

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the button platform."""
    device_id = config_entry.data[CONF_DEVICE_ID]
    async_add_entities([SunseekerEdgeCutButton(hass, device_id)])

class SunseekerEdgeCutButton(ButtonEntity):
    """Button to start edge cutting mode."""

    def __init__(self, hass, device_id):
        self.hass = hass
        self._device_id = device_id
        self._attr_has_entity_name = True
        self._attr_translation_key = "edge_cut"
        self._attr_unique_id = f"sunseeker_edge_{device_id}"
        self._attr_icon = "mdi:robot-mower"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=f"Sunseeker {device_id}",
            manufacturer="Sunseeker",
        )

    async def async_press(self):
        """Send edge cutting command."""
        topic = TOPIC_COMMAND.format(self._device_id)
        payload = json.dumps({"cmd": 101, "mode": 4})
        await mqtt.async_publish(self.hass, topic, payload)
