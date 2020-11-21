from unittest import TestCase

from rofi_tpb import cli


class TestCli(TestCase):
    def test_parse_args(self):
        args = []
        parsed = cli.parse_args(args)
        assert not hasattr(parsed, "query") and not hasattr(parsed, "category")

        args = ["-u", "https://test.com"]
        parsed = cli.parse_args(args)
        parsed.url = "https://test.com"

        args = ["search"]
        parsed = cli.parse_args(args)
        assert hasattr(parsed, "query") and not hasattr(parsed, "category")
        assert parsed.query == None

        args = ["search", "ubuntu"]
        parsed = cli.parse_args(args)
        assert hasattr(parsed, "query") and not hasattr(parsed, "category")
        assert parsed.query == "ubuntu"

        args = ["top"]
        parsed = cli.parse_args(args)
        assert not hasattr(parsed, "query") and hasattr(parsed, "category")
        assert parsed.category == None

        args = ["top", "all"]
        parsed = cli.parse_args(args)
        assert not hasattr(parsed, "query") and hasattr(parsed, "category")
        assert parsed.category == "all"

        args = ["top", "all", "-r"]
        parsed = cli.parse_args(args)
        assert not hasattr(parsed, "query") and hasattr(parsed, "category")
        assert parsed.category == "all"
        assert parsed.recent
