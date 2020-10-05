import argparse
import sys
from typing import Optional, Sequence
from urllib.request import HTTPError, URLError

from tpblite import CATEGORIES
from dynmen import MenuError

from .settings import CATEGORIES_STRINGS
from .tpb import TPB


def parse_args(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Argument parsing.

    Args:
        args: arguments.

    Returns:
        parsed arguments.
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Query ThePirateBay.")
    subparsers = parser.add_subparsers()
    parser.add_argument("-u", "--url", type=str, default=None, help="ThePirateBay url.")

    search_parser = subparsers.add_parser("search", help="Search ThePirateBay.")
    top_parser = subparsers.add_parser(
        "top", help="Browse ThePirateBay's top torrents."
    )

    search_parser.add_argument(
        "query", nargs="?", type=str, default=None, help="Search query."
    )
    top_parser.add_argument(
        "-r", "--recent", action="store_true", help="Top torrents in the last 48h."
    )
    top_parser.add_argument(
        "category",
        nargs="?",
        choices=[category.lower() for category in CATEGORIES_STRINGS],
        default=None,
        help="ThePirateBay category.",
    )
    return parser.parse_args(args)


def main():
    """Main Logic."""
    args = parse_args()

    try:
        tpb = TPB(url=args.url)
        if hasattr(args, "category"):
            # if top subparser
            if args.category is not None:
                category = getattr(CATEGORIES, args.category.upper(), None)
            else:
                category = None
            torrent = tpb.top(category=category)
        elif hasattr(args, "query"):
            # if search subparser
            torrent = tpb.search(query=args.query)
        else:
            # if not subparser
            torrent = tpb.search_or_top()

        tpb.action(torrent)
    except MenuError:
        pass
    except (URLError, HTTPError):
        print(
            f"Can't access '{args.url}', specify a different proxy with the -u flag.",
            file=sys.stderr,
        )
