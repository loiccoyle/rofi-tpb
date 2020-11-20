import shlex
from subprocess import Popen
from typing import List, Optional
from urllib.request import urlopen

from dynmen import Menu
from tpblite import CATEGORIES
from tpblite import TPB as TPBAPI
from tpblite.models.torrents import Torrent, Torrents

from .config import CONFIG
from .proxy import get_proxies
from .utils import torrent_format


class TPB:
    def __init__(self, url: Optional[str] = None):
        if url is None:
            if CONFIG["menu"].getboolean("use_tpb_proxy"):
                try:
                    url = get_proxies()[0]
                except Exception:
                    url = CONFIG["menu"]["tpb_url"]
            else:
                url = CONFIG["menu"]["tpb_url"]
        self.url = url
        if not self._check_url(self.url):
            raise ValueError(f"Cannot reach '{self.url}'.")
        self.tpb = TPBAPI(self.url)

    def get_menu(
        self,
        prompt: Optional[str] = None,
        lines: Optional[int] = None,
        multiple: bool = False,
        message: Optional[str] = None,
    ) -> Menu:
        """Create the dynamic menu object."""
        args = shlex.split(CONFIG["menu"]["command"])
        if "rofi" in args:
            if prompt is not None:
                args += ["-p", prompt]
            if lines is not None:
                args += ["-l", lines]
            if multiple:
                args += ["-multi-select"]
            if message is not None:
                args += ["-mesg", message]
        return Menu(args)

    @staticmethod
    def _check_url(url):
        return urlopen(url).getcode() == 200

    def search_or_top(self) -> str:  # pylint: disable=inconsistent-return-statements
        """Chose between top or search.

        Returns:
            Torrents matching either the search or the top category.
        """
        choices = {"Search": self.search, "Top": self.top}
        menu = self.get_menu(prompt="Select", lines=2)
        out = menu(choices)
        return out.value()

    def search(self, query: Optional[str] = None) -> Torrents:
        """Search for torrents.

        Args:
            query (optional): search query.

        Returns:
            The Torrents matching the search query.
        """
        if query is None:
            menu = self.get_menu(prompt="Search", lines=0)
            query = menu().selected
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
            categories = [
                cat.strip() for cat in CONFIG["menu"]["categories"].split(",")
            ]
            if CONFIG["menu"].getboolean("categories_48h"):
                categories += [cat + " 48h" for cat in categories]
            categories = sorted(categories)
            menu = self.get_menu(prompt="Select", lines=len(categories))
            out = menu(categories)
            category = out.selected
        last_48 = "48h" in category
        category = category.split()[0]
        category = getattr(CATEGORIES, category)
        if not isinstance(category, int):
            category = category.ALL
        torrents = self.tpb.top(category=category, last_48=last_48)
        return self.select(torrents)

    def select(self, torrents: Torrents) -> List[Torrent]:
        """Select a torrent from a `Torrents` object.

        Args:
            torrents: `Torrents`from which to select a single torrent.

        Reuturns:
            Selected torrents.
        """
        torrents_formatted = {}
        for torrent in torrents:
            torrents_formatted[
                torrent_format(CONFIG["menu"]["torrent_format"], torrent)
            ] = torrent
        menu = self.get_menu(prompt="Select", multiple=True)
        out = menu(torrents_formatted)
        selected_out = []
        for selected in out.selected.split("\n"):
            selected_out.append(torrents_formatted[selected])
        return selected_out

    def action(self, torrent: Torrent) -> None:
        """Execute an action on `Torrent`.

        Args:
            torrent: `Torrent` instance on which to run the action.
        """
        actions = CONFIG["actions"]
        menu = self.get_menu(prompt="Select", lines=len(actions), message=torrent)
        out = menu(actions)
        command = torrent_format(out.value, torrent)
        Popen(command, shell=True)
