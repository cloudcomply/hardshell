import os
import shutil
import toml
import importlib.resources as pkg_resources


def load_config(file_path):
    """
    Load the TOML configuration file.
    """
    with open(file_path, "r") as file:
        return toml.load(file)
