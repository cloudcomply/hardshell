from dataclasses import dataclass

import distro

from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.common import (
    log_and_print,
    log_status,
    pkg_mgr_apt,
    pkg_mgr_dnf,
)

if distro.id() in pkg_mgr_apt:
    import apt
elif distro.id() in pkg_mgr_dnf:
    from src.hardshell.common.dnf import base


@dataclass
class PackageCheck(BaseCheck):
    package_name: str = None
    package_installed: bool = False

    def check_apt(self):
        cache = apt.Cache()

        try:
            installed_result = "fail"
            upgrade_result = "fail"
            pkg = cache[self.package_name]
            installed = pkg.is_installed
            version = pkg.installed.version if installed else None
            upgradeable = pkg.is_upgradable

            log_and_print(
                f"package {self.package_name} is installed: {installed} with version {version}",
                log_only=True,
            )

            if installed == self.package_installed:
                log_and_print(
                    f"package {self.package_name} is {'installed' if installed else 'not installed'} and expected to be {'installed' if self.package_installed else 'not installed'}.",
                    log_only=True,
                )
            else:
                log_and_print(
                    f"package {self.package_name} is {'installed' if installed else 'not installed'} but expected to be {'installed' if self.package_installed else 'not installed'}.",
                    log_only=True,
                )

            log_and_print(
                f"package {self.package_name} is {'upgradeable' if upgradeable else 'not upgradeable'}.",
                log_only=True,
            )

            installed_result = (
                "pass" if installed and self.package_installed else "fail"
            )

            self.set_result_and_log_status(
                self.check_id,
                self.check_name,
                installed_result,
                "package installed",
                self.check_type,
            )

            upgrade_result = "pass" if not upgradeable else "fail"

            self.set_result_and_log_status(
                self.check_id,
                self.check_name,
                upgrade_result,
                "package upgradeable",
                self.check_type,
            )

        except KeyError:
            log_and_print(
                f"package {self.package_name} not found in the cache.", log_only=True
            )
        except AttributeError as e:
            log_and_print(f"an attribute error occurred: {str(e)}")

    def check_dnf(self):
        try:
            installed_result = "fail"

            # Initial Query
            query = base.sack.query()

            # Installed Query
            installed = query.installed().filter(name=self.package_name)

            # Filter by package name
            # installed = installed.filter(name=self.package_name)

            # Upgrades
            # upgrades = installed.upgrades()

            pkg_installed = list(installed)
            # pkg_upgrades = list(upgrades)

            if len(pkg_installed) == 0 and not self.package_installed:
                log_and_print(
                    f"package {self.package_name} is not installed and expected to be not installed.",
                    log_only=True,
                )
            elif len(pkg_installed) == 0 and self.package_installed:
                log_and_print(
                    f"package {self.package_name} is not installed and expected to be installed.",
                    log_only=True,
                )
                installed_result = "fail"
            else:
                for package in pkg_installed:
                    if (
                        package.name == self.package_name
                        and package.installed == self.package_installed
                    ):
                        log_and_print(
                            f"package {self.package_name} is {'installed' if package.installed else 'not installed'} and expected to be {'installed' if self.package_installed else 'not installed'}.",
                            log_only=True,
                        )
                        installed_result = "pass"
                    else:
                        log_and_print(
                            f"package {self.package_name} is {'installed' if package.installed else 'not installed'} and expected to be {'installed' if self.package_installed else 'not installed'}.",
                            log_only=True,
                        )
                        installed_result = "fail"

            self.set_result_and_log_status(
                self.check_id,
                self.check_name,
                installed_result,
                "package installed",
                self.check_type,
            )

            # TODO Check for package upgrades
            # for upgrade in pkg_upgrades:
            #     print(upgrade)

        except Exception as e:
            log_and_print(f"an error occurred: {str(e)}")

    def run_check(self, current_os, global_config):
        log_and_print(f"checking package {self.package_name}", log_only=True)

        if current_os["id"] in pkg_mgr_apt:
            log_and_print(f"package manager is apt", log_only=True)
            self.check_apt()
        elif current_os["id"] in pkg_mgr_dnf:
            log_and_print(f"package manager is dnf", log_only=True)
            self.check_dnf()
        else:
            log_and_print(f"unsupported os: {current_os['id']}", log_only=True)
