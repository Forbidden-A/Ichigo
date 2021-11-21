from ichigo.config.models import Config
import yaml
import logging
from dotenv import load_dotenv

__all__ = ["load_config_file", "deserialise_raw_config"]

_LOGGER = logging.getLogger(__name__)


def load_config_file(config_file_path: str) -> dict:
    """
    Safely loads the given config file with PyYAML.
    Raises an exception if the file isn't found, naturally.
    """
    _LOGGER.debug("Loading raw config file")

    with open(config_file_path) as fp:
        return yaml.safe_load(fp)


def deserialise_raw_config(raw_data: dict = {}, do_load_dotenv: bool = False) -> Config:

    if do_load_dotenv:
        load_dotenv(override=True)

    clean_data = {
        key: value for key, value in raw_data.items() if None not in (key, value)
    }
    return Config.from_dict(clean_data)
