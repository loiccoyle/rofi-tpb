from configparser import ConfigParser
from pathlib import Path
from shutil import rmtree
from unittest import TestCase

from rofi_tpb import config, settings


class TestConfig(TestCase):
    def setUp(self):
        self.test_dir = Path() / "test_config"
        if not self.test_dir.is_dir():
            self.test_dir.mkdir()
        self.test_config = self.test_dir / "config.ini"

    def test_write_default(self):
        config.write_default(self.test_config)
        assert self.test_config.is_file()

    def test_load_config(self):
        config.write_default(self.test_config)
        loaded = config.load_config(self.test_config)
        parser = ConfigParser()
        parser.read_dict(settings.DEFAULT_CONFIG)
        assert loaded == parser

    def tearDown(self):
        if self.test_dir.is_dir():
            rmtree(self.test_dir)
