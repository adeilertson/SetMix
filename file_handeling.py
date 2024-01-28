import logging
import logging.config
import yaml
from pathlib import Path


def set_logger():
    """Sets logging details from external config file

    Expects configured log settings at 'config/logging.yml'

    Returns:
        obj: Configured logger
    """
    log_cfg_file = Path() / 'config' / 'logging.yml'
    with open(log_cfg_file, 'r') as f:
        log_cfg = yaml.safe_load(f.read())
        logging.config.dictConfig(log_cfg)

    logger = logging.getLogger('primary')

    return logger


def get_config():
    """Loads config data from external config file

    Expects config file at 'config/config.yml'
    Required fields:
    - setlist_fm_api_key: API KEY
    - testing: True/False
    - spotify_api_key: API KEY

    Returns:
        dict: Configured settings
    """
    cfg_file = Path() / 'config' / 'config.yml'
    with open(cfg_file, 'r') as f:
        cfg = yaml.safe_load(f.read())

    return cfg
