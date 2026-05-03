import logging
from datetime import timedelta
import aiohttp
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class PelicanDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, session, url, api_key):
        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=UPDATE_INTERVAL)
        )
        self.session = session
        self.url = url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "HomeAssistant/PelicanPanelIntegration"
        }

    async def _async_update_data(self):
        try:
            # 1. Alle Server abrufen
            async with self.session.get(f"{self.url}/api/client", headers=self.headers) as resp:
                resp.raise_for_status()
                servers_data = await resp.json()

            server_info = {}
            # 2. Für jeden Server Details abrufen
            for srv in servers_data.get("data", []):
                uid = srv["attributes"]["identifier"]
                srv_base_attr = srv.get("attributes", {})
                
                # Standard-Werte für Ressourcen (Fallback, falls Server 409 wirft)
                res_data = {
                    "attributes": {
                        "current_state": "offline",
                        "resources": {
                            "cpu_absolute": 0, "memory_bytes": 0, "disk_bytes": 0,
                            "network_rx_bytes": 0, "network_tx_bytes": 0, "uptime": 0
                        }
                    }
                }
                
                # Vorab prüfen, ob der Server gesperrt oder im Installationsprozess ist
                if srv_base_attr.get("is_suspended"):
                    res_data["attributes"]["current_state"] = "suspended"
                elif srv_base_attr.get("is_installing"):
                    res_data["attributes"]["current_state"] = "installing"

                # Ressourcen abrufen (mit Crash-Schutz für 409 Conflict)
                try:
                    async with self.session.get(f"{self.url}/api/client/servers/{uid}/resources", headers=self.headers) as res_resp:
                        res_resp.raise_for_status()
                        res_data = await res_resp.json()
                except aiohttp.ClientResponseError as e:
                    if e.status == 409:
                        _LOGGER.warning(f"Server {uid} antwortet mit 409 (Offline/Gesperrt/Installiert). Überspringe Ressourcen-Abfrage.")
                    else:
                        raise e

                # Server Details abrufen (inkl. Egg und Ports)
                async with self.session.get(f"{self.url}/api/client/servers/{uid}?include=egg,allocations", headers=self.headers) as detail_resp:
                    detail_resp.raise_for_status()
                    detail_data = await detail_resp.json()
                
                srv_attr = detail_data.get("attributes", {})

                # Allocations zählen
                allocations = srv_attr.get("relationships", {}).get("allocations", {}).get("data", [])
                alloc_count = len(allocations)

                # Den echten Egg-Namen auslesen
                egg_name = "Unbekannt"
                egg_rel = srv_attr.get("relationships", {}).get("egg", {})
                
                if "attributes" in egg_rel:
                    egg_name = egg_rel["attributes"].get("name", "Unbekannt")
                elif "data" in egg_rel and "attributes" in egg_rel.get("data", {}):
                    egg_name = egg_rel["data"]["attributes"].get("name", "Unbekannt")
                elif "name" in egg_rel:
                    egg_name = egg_rel.get("name", "Unbekannt")

                # Docker Image URL kürzen (aus "ghcr.io/parkervcp/yolks:java_21" wird "yolks:java_21")
                raw_image = srv_attr.get("docker_image", "Unbekannt")
                short_image = raw_image.split("/")[-1] if "/" in raw_image else raw_image

                # Fallback für das Egg (falls API leer ist)
                if egg_name == "Unbekannt" or not egg_name:
                    egg_name = short_image

                server_info[uid] = {
                    "name": srv_attr.get("name", "Unbekannt"),
                    "uuid": uid,
                    "limits": srv_attr.get("limits", {}),
                    "features": srv_attr.get("feature_limits", {}),
                    "resources": res_data.get("attributes", {}).get("resources", {}),
                    "state": res_data.get("attributes", {}).get("current_state", "unknown"),
                    "egg": egg_name,
                    "image": short_image,  # Hier wird jetzt das gekürzte Image übergeben
                    "allocations": alloc_count
                }
            return server_info
        except Exception as e:
            raise UpdateFailed(f"Fehler bei API Abfrage: {e}")