import ctypes
import glob
import os
import platform
import re
from pathlib import Path
from typing import Callable, Dict, Union

from src.hardshell import __name__, __version__
from src.hardshell.common.logging import logger


def detect_admin() -> bool:
    """
    Detect if the script has admin/root privileges.

    Returns:
        bool: True if admin, False otherwise.

    Raises:
        NotImplementedError: If the system is not supported.

    Example Usage:
        is_admin = detect_admin()
        print(is_admin)  # True or False
    """

    # Define platform-specific admin checkers
    platform_checkers: Dict[str, Callable[[], bool]] = {
        "Windows": lambda: ctypes.windll.shell32.IsUserAnAdmin() == 1,
        "Linux": lambda: os.geteuid() == 0,
    }

    # Get the current system platform
    system = platform.system()

    # Get the checker function for the current system
    checker = platform_checkers.get(system)

    if checker is None:
        raise NotImplementedError(f"System '{system}' is not supported...")

    return checker()


def detect_os() -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Detect the operating system

    Returns:
        dict: operating system details

    Raises:
        FileNotFoundError: If file /etc/os-release not found
    """

    def detect_windows() -> Dict[str, str]:
        """Detect details for Windows OS and return them as a dictionary."""
        return {
            "name": platform.system(),
            "type": platform.system().lower(),
            "version": platform.release(),
            "full_version": platform.version(),
            "node": platform.node(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }

    def detect_linux() -> Dict[str, str]:
        """Detect details for Linux/Unix-like OS and return them as a dictionary."""
        os_release = {}
        path = Path("/etc/os-release")

        try:
            if path.exists():
                with path.open() as f:
                    content = f.read()
                for line in content.strip().split("\n"):
                    key, value = line.split("=", 1)
                    os_release[key.lower()] = value.strip('"')
                os_release["type"] = "linux"
            else:
                os_release = {"Error": "File /etc/os-release not found"}
        except FileNotFoundError:
            os_release = {"Error": "File /etc/os-release not found"}
        except Exception as error:
            os_release = {"Error": f"An error occurred: {error}"}

        return os_release

    os_detectors: Dict[str, Callable[[], Dict[str, str]]] = {
        "Windows": detect_windows,
        "Linux": detect_linux,
    }

    system = platform.system()

    return os_detectors.get(system, lambda: {"Error": "Unsupported OS..."})()


def find_pattern_in_directory(directory, pattern, extension=None):
    """Find the pattern in the files in a given directory."""
    pattern_found = False
    pattern_line = ""

    paths = glob.glob(os.path.join(directory, "*"))

    if extension:
        files = [f for f in paths if os.path.isfile(f) and f.endswith(extension)]
    else:
        files = [f for f in paths if os.path.isfile(f)]

    directories = [f for f in paths if os.path.isdir(f)]

    for file in files:
        found, line = find_pattern_in_file(file, pattern)
        if found:
            pattern_found = True
            pattern_line = line
            break

    for dir in directories:
        found, line = find_pattern_in_directory(dir, pattern, extension)
        if found:
            pattern_found = True
            pattern_line = line
            break

    return pattern_found, pattern_line


def find_pattern_in_file(path, pattern):
    """Search for the parameter in the given file."""
    pattern_found = False
    pattern_line = ""
    try:
        with open(path, "r") as f:
            for line in f:
                if re.search(pattern, line, flags=re.IGNORECASE):
                    pattern_found = True
                    pattern_line = line.strip()
    except IOError:
        print(f"Could not read file: {path}")
    return pattern_found, pattern_line


def get_config_mapping(config_name, global_config):
    attribute_path = config_mapping.get(config_name)
    if attribute_path:
        attrs = attribute_path.split(".")
        value = global_config
        for attr in attrs:
            value = getattr(value, attr, None)
            if value is None:
                break
        return value


def log_and_print(message, level="info", log_only=False):
    if not log_only:
        print(message)
    getattr(logger, level)(message)


def path_exists(path):
    return os.path.exists(path)


def shutdown_banner():
    pass


def startup_banner():
    """
    Gets the startup banner.

    Returns:
        list: str

    Example Usage:
        banner = get_banner()
        print(banner)  # Prints startup banner
    """
    banner = []
    banner.append(" " * 2 + "#" * 90)
    banner.append(" " * 2 + f"# {__name__} {__version__}")
    banner.append(" " * 2 + "# " + "-" * 15)
    banner.append(
        " " * 2
        + f"# {__name__} comes with ABSOLUTELY NO WARRANTY. This is free software, and"
    )
    banner.append(
        " " * 2
        + "# you are welcome to redistribute it under the terms of the MIT License."
    )
    banner.append(
        " " * 2 + "# See the LICENSE file for details about using this software."
    )
    banner.append(" " * 2 + "#" * 90 + "\n")
    return banner


def strip_non_alphabetical(s):
    """Remove all non-alphabetical characters from the string."""
    # Replace non-alphabetical characters with an empty string
    return re.sub(r"[^a-zA-Z]", "", s)


config_mapping = {
    "chrony": "config_files.chrony",
    "coredump": "config_files.coredump",
    "crypto-policies": "config_files.crypto_policies",
    "gpg": "config_files.gpg",
    "kernel": "config_files.kernel",
    "selinux": "config_files.selinux",
    "shell": "config_files.shell",
    "sshd": "config_files.sshd",
    "sudo": "config_files.sudo",
    "sysctl": "config_files.sysctl",
    "umask": "config_files.umask",
}


pkg_mgr_apt = ["ubuntu"]
pkg_mgr_dnf = ["fedora"]

# Old Code
# def get_pkgmgr_mapping(global_config, os_name):
#     attribute_path = pkgmgr_mapping.get(os_name)
#     if attribute_path:
#         attrs = attribute_path.split(".")
#         value = global_config
#         for attr in attrs:
#             value = getattr(value, attr, None)
#             if value is None:
#                 break
#         return value

# pkgmgr_mapping = {
#     "amzn": "pkgmgr.amzn",
#     # "debian": "pkgmgr.debian",
#     # "fedora": "pkgmgr.fedora",
#     # "kali": "pkgmgr.kali",
#     # "rhel": "pkgmgr.rhel",
#     # "rocky": "pkgmgr.rocky",
#     "ubuntu": "pkgmgr.ubuntu",
# }
