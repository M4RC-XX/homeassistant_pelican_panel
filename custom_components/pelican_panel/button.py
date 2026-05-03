from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for server_id in coordinator.data:
        entities.append(PelicanPowerButton(coordinator, server_id, "Start", "start", "mdi:play"))
        entities.append(PelicanPowerButton(coordinator, server_id, "Stop", "stop", "mdi:stop"))
        entities.append(PelicanPowerButton(coordinator, server_id, "Restart", "restart", "mdi:restart"))

    async_add_entities(entities)

class PelicanPowerButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, server_id, name, action, icon):
        super().__init__(coordinator)
        self.server_id = server_id
        self.action = action
        self._attr_name = f"{coordinator.data[server_id]['name']} {name}"
        self._attr_unique_id = f"pelican_{server_id}_{action}"
        self._attr_icon = icon

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.server_id)},
            "name": self.coordinator.data[self.server_id]['name'],
            "manufacturer": "Pelican Panel"
        }

    async def async_press(self) -> None:
        url = f"{self.coordinator.url}/api/client/servers/{self.server_id}/power"
        payload = {"signal": self.action}
        
        async with self.coordinator.session.post(url, headers=self.coordinator.headers, json=payload) as resp:
            resp.raise_for_status()
        
        await self.coordinator.async_request_refresh()