import os
import yaml


class ConfigFormatError(Exception):
    pass


class ConfigNotFoundError(Exception):
    pass


_default_config = {
    "tests": [],
    "history_limit": 100,
}


_config_types = {
    "tests": list,
    "history_limit": int,
}


def load_user_config(vcs):
    """Load the user config

    Args:
        vcs (easyci.vcs.base.Vcs) - the vcs object for the current project

    Returns:
        dict - the config

    Raises:
        ConfigFormatError
        ConfigNotFoundError
    """
    config_path = os.path.join(vcs.path, 'eci.yaml')
    if not os.path.exists(config_path):
        raise ConfigNotFoundError
    with open(config_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError:
            raise ConfigFormatError
    if not isinstance(config, dict):
        raise ConfigFormatError
    for k, v in _default_config.iteritems():
        config.setdefault(k, v)
    for k, v in _config_types.iteritems():
        if not isinstance(config[k], v):
            raise ConfigFormatError
    return config
