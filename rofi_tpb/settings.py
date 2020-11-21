import os
from pathlib import Path
from random import choice

CONFIG_DIR = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / "rofi-tpb"
CONFIG_FILE = CONFIG_DIR / "config.ini"

DEFAULT_CONFIG = {
    "menu": {
        "command": "rofi -dmenu -i",
        "torrent_format": "{title:<65} 📁{filesize:<12} 🔽{seeds:<4} 🔼{leeches:<4} Trusted:{trusted} VIP:{vip}",
        "vip_str": "✅",
        "not_vip_str": "❌",
        "trusted_str": "✅",
        "not_trusted_str": "❌",
        "use_tpb_proxy": True,
        "tpb_url": "https://thepiratebay0.org",
        "categories": "All, APPLICATIONS, AUDIO, GAMES, OTHER, PORN, VIDEO",
        "categories_48h": True,
    },
    "actions": {"add": "xdg-open '{magnetlink}'", "open": "xgd-open '{url}'"},
}

PROXY_URL = "https://piratebayproxy.info/"

USER_AGENTS = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/60.0.3112.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/60.0.3112.113 Safari/537.36",
)

HEADERS = {"User-Agent": choice(USER_AGENTS)}

CATEGORIES_STRINGS = [
    "ALL",
    "APPLICATIONS",
    "AUDIO",
    "GAMES",
    "OTHER",
    "PORN",
    "VIDEO",
]
