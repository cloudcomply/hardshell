from dataclasses import dataclass

import apt

# import dnf

from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.common import log_and_print
from src.hardshell.common.dnf import installed


@dataclass
class PackageCheck(BaseCheck):
    package_name: str = None
    package_installed: bool = False

    def check_apt(self):
        cache = apt.Cache()

        try:
            pkg = cache[self.package_name]
            installed = pkg.is_installed
            version = pkg.installed.version if installed else None
            upgradeable = pkg.is_upgradable

            log_and_print(
                f"Package {self.package_name} is installed: {installed} with version {version}"
            )

            if installed == self.package_installed:
                log_and_print(
                    f"Package {self.package_name} is {'installed' if installed else 'not installed'} and expected to be {'installed' if self.package_installed else 'not installed'}."
                )
            else:
                log_and_print(
                    f"Package {self.package_name} is {'installed' if installed else 'not installed'} but expected to be {'installed' if self.package_installed else 'not installed'}."
                )

            log_and_print(
                f"Package {self.package_name} is {'upgradeable' if upgradeable else 'not upgradeable'}."
            )

        except KeyError:
            log_and_print(f"Package {self.package_name} not found in the cache.")
        except AttributeError as e:
            log_and_print(f"An attribute error occurred: {str(e)}")

    def check_dnf(self):
        try:
            pkg_installed = installed(self.package_name)

            print(pkg_installed)
        except Exception as e:
            log_and_print(f"An error occurred: {str(e)}")
        # except KeyError:
        #     log_and_print(f"Package {self.package_name} not found in the cache.")
        # except AttributeError as e:
        #     log_and_print(f"An attribute error occurred: {str(e)}")

    def run_check(self, current_os, global_config):
        log_and_print(f"Checking package {self.package_name}")
        pkg_mgr_apt = ["ubuntu"]
        pkg_mgr_dnf = ["amzn"]

        if current_os["id"] in pkg_mgr_apt:
            log_and_print(f"Package manager is apt")
            self.check_apt()
        elif current_os["id"] in pkg_mgr_dnf:
            log_and_print(f"Package manager is dnf")
            self.check_dnf()
        else:
            log_and_print(f"Unsupported OS: {current_os['id']}")


# Old Code
# def check_apt(self):
#     installed = False
#     version = None

#     cache = apt.Cache()

#     try:
#         pkg = cache[self.package_name]

#         log_and_print(
#             f"Package {self.package_name} is installed: {pkg.is_installed} with version {pkg.installed}"
#         )

#         installed = pkg.is_installed
#         upgradeable = pkg.is_upgradable
#         version = pkg.installed

#         if installed == self.package_installed:
#             log_and_print(
#                 f"Package {self.package_name} is installed and expected to be installed."
#             )
#         elif installed and not self.package_installed:
#             log_and_print(
#                 f"Package {self.package_name} is installed but not expected to be installed."
#             )
#         elif not installed and self.package_installed:
#             log_and_print(
#                 f"Package {self.package_name} is not installed but expected to be installed."
#             )
#         elif not installed and not self.package_installed:
#             log_and_print(
#                 f"Package {self.package_name} is not installed and not expected to be installed."
#             )

#         if upgradeable:
#             log_and_print(f"Package {self.package_name} is upgradeable.")
#         else:
#             log_and_print(f"Package {self.package_name} is not upgradeable.")

#     except AttributeError as e:
#         pass
#     except KeyError as e:
#         pass
