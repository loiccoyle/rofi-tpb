import configparser
from pathlib import Path

from .settings import CONFIG_FILE, DEFAULT_CONFIG

def write_default(config_path: Path) -> None:
    """Write the default config to file."""
    parser = configparser.ConfigParser()
    parser.read_dict(DEFAULT_CONFIG)
    with config_path.open("w") as fp:
        parser.write(fp)


def load_config(config_path: Path) -> configparser.ConfigParser:
    """Parse the config and return the ConfigParser instance.

    Returns:
        Parsed ConfigPraser instance.
    """
    parser = configparser.ConfigParser()
    parser.read_dict(DEFAULT_CONFIG)
    parser.read(config_path)
    return parser


CONFIG = load_config(CONFIG_FILE)
