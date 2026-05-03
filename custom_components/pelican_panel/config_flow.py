import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_PANEL_URL, CONF_API_KEY

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_PANEL_URL, description="Panel URL (z.B. https://panel.deinedomain.de)"): str,
    vol.Required(CONF_API_KEY, description="Client API Key"): str,
})

class PelicanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Pelican Panel", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )