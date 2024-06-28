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
        self.set_result_and_log_status(
            log_message=f"checking for /bin/true entries for module {module_name}",
            log_only=True,
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
                            self.set_result_and_log_status(
                                log_message=f"found /bin/true entry in {filepath}",
                                log_only=True,
                            )
                            bin_true = True
                            break
            if bin_true:
                break
        self.set_result_and_log_status(
            check_id=self.check_id,
            check_message="module /bin/true entry",
            check_name=self.check_name,
            check_result="pass" if bin_true == self.module_loadable else "fail",
            check_type=self.check_type,
            log_message=f"module {module_name} has /bin/true entry: {bin_true}",
        )
        return bin_true

    def check_bin_false_entries(self, modprobe_dir, module_name):
        self.set_result_and_log_status(
            log_message=f"checking if module {module_name} has a /bin/false entry",
            log_only=True,
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
                            self.set_result_and_log_status(
                                log_message=f"found /bin/false entry in {filepath}",
                                log_only=True,
                            )
                            bin_false = True
                            break
            if bin_false:
                break
        self.set_result_and_log_status(
            check_id=self.check_id,
            check_message="module /bin/false entry",
            check_name=self.check_name,
            check_result="pass" if bin_false == self.module_loadable else "fail",
            check_type=self.check_type,
            log_message=f"module {module_name} has /bin/false entry: {bin_false}",
        )
        return bin_false

    def check_deny_listed(self, modprobe_dir, module_name):
        self.set_result_and_log_status(
            log_message=f"checking if module {module_name} is deny listed",
            log_only=True,
        )
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
                            self.set_result_and_log_status(
                                log_message=f"found blacklist entry in {filepath}",
                                log_only=True,
                            )
                            deny_listed = True
                            break
            if deny_listed:
                break
        self.set_result_and_log_status(
            check_id=self.check_id,
            check_message="module deny listed",
            check_name=self.check_name,
            check_result="pass" if deny_listed == self.module_denied else "fail",
            check_type=self.check_type,
            log_message=f"module {module_name} is deny listed: {deny_listed}",
        )
        return deny_listed

    def is_module_available(self, module_name, module_path):
        self.set_result_and_log_status(
            log_message=f"checking if module {module_name} is available", log_only=True
        )
        available = False
        for root, dirs, files in os.walk(module_path):
            if f"{module_name}.ko" in files:
                available = True
                break
        self.set_result_and_log_status(
            log_message=f"module {module_name} is available: {available}", log_only=True
        )
        return available

    def is_module_loaded(self, module_name):
        self.set_result_and_log_status(
            log_message=f"checking if module {module_name} is loaded", log_only=True
        )
        try:
            lsmod_output = subprocess.check_output(["lsmod"], text=True)
            is_module_in_lsmod = module_name in lsmod_output
            self.set_result_and_log_status(
                check_id=self.check_id,
                check_message="module loaded",
                check_name=self.check_name,
                check_result=(
                    "pass" if is_module_in_lsmod == self.module_loaded else "fail"
                ),
                check_type=self.check_type,
                log_message=f"module {module_name} is {'loaded' if is_module_in_lsmod else 'not loaded'}",
            )
            return module_name in lsmod_output
        except subprocess.CalledProcessError:
            return False

    def is_module_precompiled(self, boot_config_path, module_name):
        self.set_result_and_log_status(
            log_message=f"checking if module {module_name} is precompiled",
            log_only=True,
        )
        if os.path.isfile(boot_config_path):
            with open(boot_config_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith(f"CONFIG_{module_name.upper()}=y"):
                        self.set_result_and_log_status(
                            log_message=f"module {module_name} is precompiled",
                            log_only=True,
                        )
                        return True
                    else:
                        self.set_result_and_log_status(
                            log_message=f"module {module_name} is not precompiled",
                            log_only=True,
                        )
                        return False

    def run_check(self, current_os, global_config):
        self.set_result_and_log_status(
            log_message=f"checking module {self.module_name}", log_only=True
        )

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
            else:
                self.set_result_and_log_status(
                    check_id=self.check_id,
                    check_message="module not available",
                    check_name=self.check_name,
                    check_result="skip",
                    check_type=self.check_type,
                    log_message=f"module {self.module_name} is not available, skipping checks",
                )

        else:
            self.set_result_and_log_status(
                check_id=self.check_id,
                check_message="module precompiled",
                check_name=self.check_name,
                check_result="skip",
                check_type=self.check_type,
                log_message=f"module {self.module_name} is precompiled, skipping checks",
            )
