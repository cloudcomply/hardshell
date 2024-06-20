import os
import re
import glob
from dataclasses import dataclass, field
from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.logging import logger


class ModuleCheck(BaseCheck):
    def __init__(self, module_name, module_type, **kwargs):
        super().__init__(**kwargs)
        self.denied = None
        self.exists = None
        self.loadable = None
        self.loaded = None
        self.module_name = module_name
        self.module_type = module_type
        self.module_base_path = f"/lib/modules/**/kernel/{self.module_type}"
        self.module_name_path = self.module_name.replace("-", "_")
        self.module_directory = self.module_name.replace("-", "/")
        self.config_paths = [
            "/etc/modprobe.d/*.conf",
            "/lib/modprobe.d/*.conf",
            "/run/modprobe.d/*.conf",
            "/usr/local/lib/modprobe.d/*.conf",
        ]

    def read_file(self, path):
        try:
            with open(path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return None

    def check_loadable(self):
        # Simulate modprobe -n -v
        loadable = self.read_file(
            f"/lib/modules/$(uname -r)/kernel/{self.module_type}/{self.module_directory}/{self.module_name}.ko"
        )
        logger.info(f"Checking if module {self.module_name} is loadable: {loadable}")
        print(f"Checking if module {self.module_name} is loadable: {loadable}")
        if loadable:
            if len(loadable.splitlines()) > 1:
                loadable = re.findall(
                    r"(^\s*install|\b{}\b)".format(self.module_name), loadable
                )
            if re.search(r"^\s*install /bin/(true|false)", loadable):
                logger.info(
                    f"Module {self.module_name} is not loadable due to dependency on /bin/true or /bin/false"
                )
                self.loadable = False
            else:
                logger.info(
                    f"Module {self.module_name} is loadable due to no dependencies"
                )
                self.loadable = True
        else:
            logger.info(
                f"Module {self.module_name} is not loadable due to not being found"
            )
            self.loadable = False

    def check_loaded(self):
        # Simulate lsmod
        loaded = self.read_file("/proc/modules")
        if loaded and self.module_name in loaded:
            logger.info(
                f"Module {self.module_name} is loaded due to being in /proc/modules"
            )
            self.loaded = True
        else:
            logger.info(
                f"Module {self.module_name} is not loaded due to not being in /proc/modules"
            )
            self.loaded = False
        return self.loaded

    def check_deny(self):
        for search_path in self.config_paths:
            for conf_file in glob.glob(search_path):
                config = self.read_file(conf_file)
                if config and re.search(
                    r"^\s*blacklist\s+{}\b".format(self.module_name),
                    config,
                    re.MULTILINE,
                ):
                    logger.info(
                        f"Module {self.module_name} is denied due to being in {conf_file}"
                    )
                    self.denied = True
                    break
                else:
                    logger.info(
                        f"Module {self.module_name} is not denied due to not being in {conf_file}"
                    )
                    self.denied = False
        return self.denied

    def run_check(self):
        logger.info(f"Checking module {self.module_name}")
        # print(glob.glob(self.module_base_path))
        for moddir in glob.glob(self.module_base_path):
            # print(moddir)
            if os.path.isdir(
                os.path.join(moddir, self.module_directory)
            ) and os.listdir(os.path.join(moddir, self.module_directory)):
                self.exists = True
                if self.denied == None:
                    self.check_deny()
                # self.check_loadable()
                # self.check_loaded()
                if (
                    moddir
                    == f"/lib/modules/{os.uname().release}/kernel/{self.module_type}"
                ):
                    self.check_loadable()
                    self.check_loaded()
            else:
                logger.info(
                    f"Module {self.module_name} does not exist due to not being in {moddir}"
                )
                self.exists = False

    def get_status(self):
        return self.denied, self.exists, self.loadable, self.loaded
