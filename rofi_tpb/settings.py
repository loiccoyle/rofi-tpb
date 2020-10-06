import os
from pathlib import Path
from random import choice
from shutil import which
from typing import Dict

CONFIG_DIR = Path(os.getenv("XDG_CONFIG_HOME"), Path.home() / ".config") / "rofi-tpb"
CONFIG_FILE = CONFIG_DIR / "config.ini"

DEFAULT_CONFIG = {
    "menu": {
        "command": "rofi -dmenu -i",
        "torrent_format": "{title:<70} 📁{filesize:<10} 🔽{seeds:<4} 🔼{leeches:<4}",
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
