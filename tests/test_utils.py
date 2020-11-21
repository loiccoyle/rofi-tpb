from pathlib import Path
from unittest import TestCase

from tpblite.models.torrents import Torrents

from rofi_tpb import utils

HTML_PATH = Path(__file__).parent / "data" / "torrents.html"


class TestUtils(TestCase):
    def setUp(self):
        with open(HTML_PATH, "r") as fp:
            contents = fp.read()
        self.torrents = Torrents(contents)

    def test_torrent_format(self):
        test_string = "{title:<65}|{filesize:<12}|{seeds:<4}|{leeches:<4}|Trusted: {trusted}|VIP: {vip}"
        for torrent in self.torrents:
            string = utils.torrent_format(test_string, torrent)
            splits = string.split("|")
            assert len(splits) == 6
