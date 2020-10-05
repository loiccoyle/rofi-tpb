from subprocess import Popen
from typing import Optional
from urllib.request import urlopen

from dynmen.rofi import Rofi
from tpblite import CATEGORIES
from tpblite import TPB as TPBAPI
from tpblite.models.torrents import Torrent, Torrents

from .proxy import get_proxies
from .settings import CATEGORIES_STRINGS, DEFAULT_KWARGS, ENTRY_FMT, get_actions
from .utils import torrent_format


class TPB:
    def __init__(self, url: Optional[str] = None):
        if url is None:
            try:
                url = get_proxies()[0]
            except Exception:
                url = "https://thepiratebay0.org"
        self.url = url
        if not self._check_url(self.url):
            raise ValueError(f"Cannot reach '{self.url}'.")
        self.tpb = TPBAPI(self.url)

    def get_menu(self):
        return Rofi(**DEFAULT_KWARGS)

    @staticmethod
    def _check_url(url):
        return urlopen(url).getcode() == 200

    def search_or_top(self) -> str:  # pylint: disable=inconsistent-return-statements
        """Chose between top or search.

        Returns:
            Torrents matching either the search or the top category.
        """
        choices = {"Search": self.search, "Top": self.top}
        rofi = self.get_menu()
        rofi.lines = 2
        rofi.prompt = "Select"
        out = rofi(choices)
        return out.value()

    def search(self, query: Optional[str] = None) -> Torrents:
        """Search for torrents.

        Args:
            query (optional): search query.

        Returns:
            The Torrents matching the search query.
        """
        if query is None:
            rofi = self.get_menu()
            rofi.lines = 0
            rofi.prompt = "Search"
            query = rofi()
        torrents = self.tpb.search(query.selected)
        return self.select(torrents)

    def top(self, category: Optional[int] = None) -> Torrents:
        """Get the top torrents for a category.

        Args:
            category (optional): top category.

        Returns:
            The torrents for the selected categories.
        """
        if category is None:
            categories = CATEGORIES_STRINGS.copy()
            categories += [cat + " 48h" for cat in CATEGORIES_STRINGS]
            categories = sorted(categories)
            rofi = self.get_menu()
            rofi.lines = len(categories)
            rofi.prompt = "Select"
            out = rofi(categories)
            category = out.selected
        last_48 = "48h" in category
        category = category.split()[0]
        category = getattr(CATEGORIES, category)
        if not isinstance(category, int):
            category = category.ALL
        torrents = self.tpb.top(category=category, last_48=last_48)
        return self.select(torrents)

    def select(self, torrents: Torrents) -> Torrent:
        """Select a torrent from a `Torrents` object.

        Args:
            torrents: `Torrents`from which to select a single torrent.

        Reuturns:
            Selected torrent.
        """
        torrents_formatted = {}
        for torrent in torrents:
            torrents_formatted[torrent_format(ENTRY_FMT, torrent)] = torrent
        rofi = self.get_menu()
        rofi.prompt = "Select"
        out = rofi(torrents_formatted)
        return out.value

    def action(self, torrent: Torrent) -> None:
        """Execute an action on `Torrent`.

        Args:
            torrent: `Torrent` instance on which to run the action.
        """
        actions = get_actions()
        rofi = self.get_menu()
        rofi.prompt = "Select"
        rofi.lines = len(actions)
        out = rofi(actions)
        command = torrent_format(out.value, torrent)
        Popen(command, shell=True)
