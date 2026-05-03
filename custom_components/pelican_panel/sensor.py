from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import PERCENTAGE
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for server_id in coordinator.data:
        entities.append(PelicanSensor(coordinator, server_id, "Status", "state", None, "mdi:server"))
        entities.append(PelicanSensor(coordinator, server_id, "CPU Usage", "resources.cpu_absolute", PERCENTAGE, "mdi:cpu-64-bit"))
        entities.append(PelicanSensor(coordinator, server_id, "Memory Usage", "resources.memory_bytes", "GB", "mdi:memory"))
        entities.append(PelicanSensor(coordinator, server_id, "Disk Usage", "resources.disk_bytes", "GB", "mdi:harddisk"))
        entities.append(PelicanSensor(coordinator, server_id, "Network In", "resources.network_rx_bytes", "MB", "mdi:download-network"))
        entities.append(PelicanSensor(coordinator, server_id, "Network Out", "resources.network_tx_bytes", "MB", "mdi:upload-network"))
        entities.append(PelicanSensor(coordinator, server_id, "Uptime", "resources.uptime", None, "mdi:clock-outline"))
        
        entities.append(PelicanSensor(coordinator, server_id, "Memory Max", "limits.memory", None, "mdi:memory")) # Icon korrigiert
        entities.append(PelicanSensor(coordinator, server_id, "Disk Max", "limits.disk", None, "mdi:harddisk-plus"))
        entities.append(PelicanSensor(coordinator, server_id, "Backups", "features.backups", None, "mdi:backup-restore"))
        entities.append(PelicanSensor(coordinator, server_id, "Databases", "features.databases", None, "mdi:database"))
        entities.append(PelicanSensor(coordinator, server_id, "Allocations", "allocations", None, "mdi:transit-connection-variant"))
        
        # Neue Text-Sensoren
        entities.append(PelicanSensor(coordinator, server_id, "Egg", "egg", None, "mdi:penguin"))
        entities.append(PelicanSensor(coordinator, server_id, "Image", "image", None, "mdi:docker"))

    async_add_entities(entities)

class PelicanSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, server_id, name, data_path, unit, icon):
        super().__init__(coordinator)
        self.server_id = server_id
        self.data_path = data_path
        self._attr_name = f"{coordinator.data[server_id]['name']} {name}"
        self._attr_unique_id = f"pelican_{server_id}_{name.replace(' ', '_').lower()}"
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.server_id)},
            "name": self.coordinator.data[self.server_id]['name'],
            "manufacturer": "Pelican Panel"
        }

    @property
    def native_value(self):
        data = self.coordinator.data[self.server_id]
        keys = self.data_path.split('.')
        val = data
        for key in keys:
            if val is not None and key in val:
                val = val[key]
            else:
                return None
        
        if val is None:
            return None

        # Custom Formatierungen
        if self.data_path in ["resources.memory_bytes", "resources.disk_bytes"]:
            return round(val / 1073741824, 2)
        if self.data_path in ["resources.network_rx_bytes", "resources.network_tx_bytes"]:
            return round(val / 1048576, 2)
        if self.data_path in ["limits.memory", "limits.disk"]:
            if val == 0:
                return "Unlimitiert"
            return f"{round(val / 1024, 2)} GB"
        if self.data_path == "resources.uptime":
            secs = val // 1000
            days = secs // 86400
            hours = (secs % 86400) // 3600
            mins = (secs % 3600) // 60
            return f"{days}t {hours}h {mins}m"

        return val