![Version](https://img.shields.io/github/v/release/M4RC-XX/homeassistant_pelican_panel?style=for-the-badge)
![Downloads](https://img.shields.io/github/downloads/M4RC-XX/homeassistant_pelican_panel/total?style=for-the-badge)
![Contributors](https://img.shields.io/github/contributors/M4RC-XX/homeassistant_pelican_panel?style=for-the-badge)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

<p align="center">
  <img src="images/logo.svg" width="100" height="100" alt="Pelican Panel Logo">
</p>

# Pelican Panel Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> [!TIP]
> **Deutschsprachige Anleitung:** Eine deutsche Version dieser Dokumentation findest du [weiter unten](#-deutsche-anleitung).

An unofficial but powerful Home Assistant integration for the Pelican Panel (and Pterodactyl forks). This integration allows you to monitor your game servers and control their power states directly from your smart home dashboard.

## ✨ Features

* **Auto-Discovery:** Automatically finds and adds all servers your account has access to.
* **Resource Monitoring:** Live updates for CPU, Memory, Disk Usage, Network In/Out, and Uptime.
* **Server Details:** Displays server limits, Docker images, used Eggs, and port allocations.
* **Power Controls:** Start, Stop, and Restart your servers via Home Assistant buttons.
* **Smart Error Handling:** Gracefully handles offline or suspended servers without breaking the integration.

---

## 🛠️ Prerequisites

To use this integration, you need to generate a **Client API Key** in your Pelican Panel:

1. Log in to your Pelican Panel (User Dashboard, **not** the Admin Control Panel).
2. Click on your account name and navigate to **Profile > API Keys**.
3. Create a new API Key.
4. **Important:** Copy the long key from the **toast notification in the top right corner** immediately. It will only be shown once! *(These keys usually start with `pacc_`).*

---

## 📦 Installation via [HACS](https://hacs.xyz/)

<a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=M4RC-XX&repository=homeassistant_pelican_panel&category=integration" target="_blank"><img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Open your Home Assistant instance and open a repository inside the Home Assistant Community Store." /></a>

1. Open Home Assistant and navigate to **HACS**.
2. Click the three dots in the top right corner and select **Custom repositories**.
3. Paste the URL of this repository and select **Integration** as the category.
4. Search for "Pelican Panel" in HACS and click **Download**.
5. **Restart** Home Assistant.

---

## ⚙️ Configuration

1. Go to **Settings -> Devices & Services**.
2. Click **Add Integration** and search for **Pelican Panel**.
3. Enter your **Panel URL** (e.g., `https://panel.yourdomain.com` - without a trailing slash).
4. Paste your newly generated **Client API Key**.
5. Click Submit. Your servers will instantly appear as devices!

---

## 🇩🇪 Deutsche Anleitung

### Voraussetzungen
Du benötigst einen **Client API Key**. Logge dich in dein Pelican Panel ein (normale Nutzeransicht, nicht der Admin-Bereich). Navigiere zu **Profile > API Keys** und erstelle einen neuen Schlüssel. 
**Wichtig:** Kopiere den extrem langen Schlüssel sofort aus der **Toast-Benachrichtigung oben rechts**, da er nur ein einziges Mal angezeigt wird! (Dieser Schlüssel beginnt in der Regel mit `pacc_`).

### Installation
Füge dieses Repository als "Benutzerdefiniertes Repository" in HACS (Kategorie: Integration) hinzu, lade es herunter und starte Home Assistant zwingend neu.

### Einrichtung
Gehe auf *Einstellungen -> Geräte & Dienste* und klicke auf *Integration hinzufügen*. Suche nach "Pelican Panel". Trage dort die URL deines Panels (ohne Schrägstrich am Ende) und deinen Client API Key ein. 

---

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

*Disclaimer: This project is not affiliated with or endorsed by Pelican Panel or Pterodactyl.*