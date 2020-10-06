import configparser

from .settings import CONFIG_FILE, DEFAULT_CONFIG


def write_default() -> None:
    """Write the default config to file."""
    parser = configparser.ConfigParser()
    parser.read_dict(DEFAULT_CONFIG)
    with CONFIG_FILE.open("w") as fp:
        parser.write(fp)


def load_config() -> configparser.ConfigParser:
    """Parse the config and return the ConfigParser instance.

    Returns:
        Parsed ConfigPraser instance.
    """
    parser = configparser.ConfigParser()
    parser.read_dict(DEFAULT_CONFIG)
    parser.read(CONFIG_FILE)
    return parser


CONFIG = load_config()
