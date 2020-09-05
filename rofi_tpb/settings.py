from random import choice
from shutil import which
from typing import Dict

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

ACTIONS = {
    "Add": "xdg-open '{magnetlink}'",
    "Open": "xdg-open '{url}'",
}

CATEGORIES_STRINGS = [
    "ALL",
    "APPLICATIONS",
    "AUDIO",
    "GAMES",
    "OTHER",
    "PORN",
    "VIDEO",
]

ENTRY_FMT = "{title:<70} 📁{filesize:<10} 🔽{seeds:<4} 🔼{leeches:<4}"


def get_atcions() -> Dict[str, str]:
    """Generate some torrent actions based on what is installed.

    Returns:
        dictionary of actions and commmands.
    """
    # peerflix
    if which("peerflix"):
        ACTIONS["Peerflix"] = "$TERMINAL -e 'peerflix '{magnetlink}''"
    return ACTIONS
