from subprocess import Popen
from typing import Optional
from urllib.request import urlopen

from rofi import Rofi
from tpblite import CATEGORIES
from tpblite import TPB as TPBAPI
from tpblite.models.torrents import Torrent, Torrents

from .exceptions import RofiClosed
from .proxy import get_proxies
from .settings import CATEGORIES_STRINGS, ENTRY_FMT, get_atcions
from .utils import torrent_format


class TPB:
    def __init__(self, url: Optional[str] = None):
        if url is None:
            try:
                url = get_proxies()[0]
            except Exception:
                url = "https://thepiratebay0.org"
        self.url = url
        self.rofi = Rofi()
        if not self._checl_url(self.url):
            raise ValueError(f"Cannot reach '{self.url}'.")
        self.tpb = TPBAPI(self.url)

    @staticmethod
    def _checl_url(url):
        return urlopen(url).getcode() == 200

    def search_or_top(self) -> str:  # pylint: disable=inconsistent-return-statements
        """Chose between top or search.

        Returns:
            Torrents matching either the search or the top category.
        """
        choices = ["Search", "Top"]
        index, key = self.rofi.select("Select", options=choices)
        if key != 0:
            raise RofiClosed()
        choice = choices[index]
        if choice == "Search":
            return self.search()
        if choice == "Top":
            return self.top()

    def search(self, query: Optional[str] = None) -> Torrents:
        """Search for torrents.

        Args:
            query (optional): search query.

        Returns:
            The Torrents matching the search query.
        """
        if query is None:
            query = self.rofi.text_entry("Search")
        if query is None:
            raise RofiClosed()
        torrents = self.tpb.search(query)
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
            index, key = self.rofi.select("Category", options=categories)
            if key != 0:
                raise RofiClosed()
            category = categories[index]
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
        torrents_formatted = []
        for torrent in torrents:
            torrents_formatted.append(torrent_format(ENTRY_FMT, torrent))
        index, key = self.rofi.select("Torrent", options=torrents_formatted)
        if key != 0:
            raise RofiClosed()
        return torrents[index]

    def action(self, torrent: Torrent) -> None:
        """Execute an action on `Torrent`.

        Args:
            torrent: `Torrent` instance on which to run the action.
        """
        actions = get_atcions()
        index, key = self.rofi.select("Action", options=actions.keys())
        if key != 0:
            raise RofiClosed()
        command = list(actions.values())[index]
        command = torrent_format(command, torrent)
        Popen(command, shell=True)
