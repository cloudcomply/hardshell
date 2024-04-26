import ctypes
import os
import platform
import re
import toml
from pathlib import Path
from typing import Callable, Dict, Union
from hardshell import __name__, __version__


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


def load_config(config_file):
    with open(config_file, "r") as f:
        config = toml.load(f)
    return config


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


def update_counts(category, passed_checks, failed_checks):
    """
    Update the counts for a specific category.

    Parameters:
    - counts (dict): The dictionary holding all count data.
    - category (str): The category under which to update the counts.
    - passed (int): The number of newly passed tests to add.
    - failed (int): The number of newly failed tests to add.
    """
    if category not in checks:
        # Initialize the category if it doesn't exist
        checks[category] = {"total": 0, "passed": 0, "failed": 0}

    # Update the counts for the specified category
    checks[category]["passed"] += passed_checks
    checks[category]["failed"] += failed_checks
    checks[category]["total"] += passed_checks + failed_checks


checks = {
    "Accounts": {"total": 0, "passed": 0, "failed": 0},
    "Aide": {"total": 0, "passed": 0, "failed": 0},
    "Audit": {"total": 0, "passed": 0, "failed": 0},
    "Banners": {"total": 0, "passed": 0, "failed": 0},
    "Filesystem-Mounts": {"total": 0, "passed": 0, "failed": 0},
    "Kernel-Modules": {"total": 0, "passed": 0, "failed": 0},
    "Kernel-Parameters": {"total": 0, "passed": 0, "failed": 0},
    "Logging-Rsyslog": {"total": 0, "passed": 0, "failed": 0},
    "Restricted-Packages": {"total": 0, "passed": 0, "failed": 0},
    "Restricted-Services": {"total": 0, "passed": 0, "failed": 0},
    "Schedulers-At": {"total": 0, "passed": 0, "failed": 0},
    "Schedulers-Cron": {"total": 0, "passed": 0, "failed": 0},
    "SELinux": {"total": 0, "passed": 0, "failed": 0},
    "Sudo": {"total": 0, "passed": 0, "failed": 0},
    "Time-Chrony": {"total": 0, "passed": 0, "failed": 0},
    "Time-Timesyncd": {"total": 0, "passed": 0, "failed": 0},
}


# Old code
# def path_exists(path):
#     if os.path.exists(path):
#         return True
#     else:
#         return False
