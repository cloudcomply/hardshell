import importlib.resources as pkg_resources
import os
import shutil

import toml


class GlobalConfig:
    def __init__(self, config_data):
        self._load_config(config_data)

    def _load_config(self, config_data):
        for key, value in config_data.items():
            if isinstance(value, dict):
                # Recursively create Config objects for nested dictionaries
                value = GlobalConfig(value)
            setattr(self, key, value)

    @classmethod
    def from_toml(cls, file_path):
        with open(file_path, "r") as f:
            config_data = toml.load(f)
        return cls(config_data)

    def __repr__(self):
        return repr(self.__dict__)


def load_config(file_path):
    """
    Load the TOML configuration file.
    """
    with open(file_path, "r") as file:
        return toml.load(file)
