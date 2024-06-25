import os
import subprocess
from dataclasses import dataclass
from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.common import log_and_print


@dataclass
class ModuleCheck(BaseCheck):
    module_name: str = None
    module_path: str = None
    module_denied: bool = None
    module_exists: bool = None
    module_loadable: bool = None
    module_loaded: bool = None

    def check_bin_true_entries(self, modprobe_dir, module_name):
        log_and_print(
            f"checking for /bin/true entries for module {module_name}", log_only=True
        )
        bin_true = False
        for filename in os.listdir(modprobe_dir):
            filepath = os.path.join(modprobe_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        if (
                            f"install {module_name} /bin/true" in line
                            and line.startswith("#") == False
                        ):
                            log_and_print(
                                f"found /bin/true entry in {filepath}",
                                log_only=True,
                            )
                            bin_true = True
                            break
            if bin_true:
                break
        self.set_result(
            self.check_id,
            self.check_name,
            "pass" if bin_true == self.module_loadable else "fail",
            "module /bin/true entry",
            self.check_type,
        )
        return bin_true

    def check_bin_false_entries(self, modprobe_dir, module_name):
        log_and_print(
            f"checking if module {module_name} has a /bin/false entry", log_only=True
        )
        bin_false = False
        for filename in os.listdir(modprobe_dir):
            filepath = os.path.join(modprobe_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        if (
                            f"install {module_name} /bin/false" in line
                            and line.startswith("#") == False
                        ):
                            log_and_print(
                                f"found /bin/false entry in {filepath}",
                                log_only=True,
                            )
                            bin_false = True
                            break
            if bin_false:
                break
        self.set_result(
            self.check_id,
            self.check_name,
            "pass" if bin_false == self.module_loadable else "fail",
            "module /bin/false entry",
            self.check_type,
        )
        return bin_false

    def check_deny_listed(self, modprobe_dir, module_name):
        log_and_print(f"checking if module {module_name} is deny listed", log_only=True)
        deny_listed = False
        for filename in os.listdir(modprobe_dir):
            filepath = os.path.join(modprobe_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        if (
                            f"blacklist {module_name}" in line
                            and line.startswith("#") == False
                        ):
                            log_and_print(
                                f"found blacklist entry in {filepath}",
                                log_only=True,
                            )
                            deny_listed = True
                            break
            if deny_listed:
                break
        self.set_result(
            self.check_id,
            self.check_name,
            "pass" if deny_listed == self.module_denied else "fail",
            "module deny listed",
            self.check_type,
        )
        return deny_listed

    def is_module_available(self, module_name, module_path):
        log_and_print(f"checking if module {module_name} is available", log_only=True)
        available = False
        for root, dirs, files in os.walk(module_path):
            if f"{module_name}.ko" in files:
                available = True
                break
        log_and_print(f"module {module_name} is available: {available}", log_only=True)
        return available

    def is_module_loaded(self, module_name):
        log_and_print(f"checking if module {module_name} is loaded", log_only=True)
        try:
            lsmod_output = subprocess.check_output(["lsmod"], text=True)
            is_module_in_lsmod = module_name in lsmod_output
            log_and_print(
                f"module {module_name} is {'loaded' if is_module_in_lsmod else 'not loaded'}",
                log_only=True,
            )
            self.set_result(
                self.check_id,
                self.check_name,
                ("pass" if is_module_in_lsmod == self.module_loaded else "fail"),
                "module loaded",
                self.check_type,
            )
            return module_name in lsmod_output
        except subprocess.CalledProcessError:
            return False

    def is_module_precompiled(self, boot_config_path, module_name):
        log_and_print(f"checking if module {module_name} is precompiled", log_only=True)
        if os.path.isfile(boot_config_path):
            with open(boot_config_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith(f"CONFIG_{module_name.upper()}=y"):
                        log_and_print(
                            f"module {module_name} is precompiled", log_only=True
                        )
                        return True
                    else:
                        log_and_print(
                            f"module {module_name} is not precompiled", log_only=True
                        )
                        return False

    def run_check(self, current_os, global_config):
        log_and_print(f"checking module {self.module_name}", log_only=True)

        boot_config_path = f"/boot/config-{os.uname().release}"
        boot_config_module_name = (
            self.module_name.replace("-", "_").replace("/", "_").upper()
        )
        modprobe_dir = "/etc/modprobe.d/"
        module_path = f"/lib/modules/{os.uname().release}/kernel"

        # check if module is precompiled
        precompiled = self.is_module_precompiled(
            boot_config_path, boot_config_module_name
        )

        if not precompiled:
            # check if module is available
            available = self.is_module_available(self.module_name, module_path)

            if available:
                # check if module is loaded
                self.is_module_loaded(self.module_name)

                # check if module is deny listed
                self.check_deny_listed(modprobe_dir, self.module_name)

                # check if module has /bin/true entries
                self.check_bin_true_entries(modprobe_dir, self.module_name)

                # check if module has /bin/false entries
                self.check_bin_false_entries(modprobe_dir, self.module_name)
