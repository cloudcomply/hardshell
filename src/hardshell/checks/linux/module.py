import glob
import os
import re
from dataclasses import dataclass
from typing import Optional
from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.logging import logger


# TODO FIX ALL OF THIS...UGH
@dataclass
class ModuleCheck(BaseCheck):
    module_name: str = None
    module_path: str = None
    module_denied: bool = None
    module_exists: bool = None
    module_loadable: bool = None
    module_loaded: bool = None

    def __post_init__(self):
        if self.module_path:
            self.module_path = (
                f"/lib/modules/{os.uname().release}/kernel/{self.module_path}"
            )

    def check_deny(self, global_config):
        is_denied = False
        for search_path in global_config.config_files.kernel:
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
                    is_denied = True
                    break
                else:
                    logger.info(
                        f"Module {self.module_name} is not denied due to not being in {conf_file}"
                    )
        # self.set_result(
        #     self.check_id,
        #     self.check_name,
        #     "pass" if self.module_denied == is_denied else "fail",
        # )

    def check_loadable(self):
        is_loadable = False
        # Simulate modprobe -n -v
        print(
            f"/lib/modules/{os.uname().release}/kernel/{self.module_path}/{self.module_name}.ko"
        )
        loadable = self.read_file(
            f"/lib/modules/{os.uname().release}/kernel/{self.module_path}/{self.module_name}.ko"
        )
        print(loadable)
        logger.info(f"Checking if module {self.module_name} is loadable: {loadable}")
        if loadable:
            if len(loadable.splitlines()) > 1:
                loadable = re.findall(
                    r"(^\s*install|\b{}\b)".format(self.module_name), loadable
                )
            if re.search(r"^\s*install /bin/(true|false)", loadable):
                logger.info(
                    f"Module {self.module_name} is not loadable due to dependency on /bin/true or /bin/false"
                )
                is_loadable = False
            else:
                logger.info(
                    f"Module {self.module_name} is loadable due to no dependencies"
                )
                is_loadable = True
        else:
            logger.info(
                f"Module {self.module_name} is not loadable due to not being found"
            )
            is_loadable = False
        # self.set_result(
        #     self.check_id,
        #     self.check_name,
        #     "pass" if self.module_loadable == is_loadable else "fail",
        # )

    def check_loaded(self):
        is_loaded = False
        # Simulate lsmod
        loaded = self.read_file("/proc/modules")
        if loaded and self.module_name in loaded:
            logger.info(
                f"Module {self.module_name} is loaded due to being in /proc/modules"
            )
            is_loaded = True
        else:
            logger.info(
                f"Module {self.module_name} is not loaded due to not being in /proc/modules"
            )
            is_loaded = False
        # self.set_result(
        #     self.check_id,
        #     self.check_name,
        #     "pass" if self.module_loaded == is_loaded else "fail",
        # )

    def read_file(self, path):
        try:
            with open(path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return None

    def run_check(self, current_os, global_config):
        logger.info(f"Checking module {self.module_name}")
        # print(self.module_path)
        # print(
        #     f"/lib/modules/{os.uname().release}/kernel/{self.module_path}/{self.module_name}.ko"
        # )

        print(glob.glob(self.module_path))
        # print(glob.glob(os.path.join()))

        for path in glob.glob(self.module_path):
            print(path)

            # self.check_deny(global_config=global_config)
            # self.check_loadable()
            # self.check_loaded()

            module_dir = os.path.join(path, self.module_path)
            print(module_dir)

            print(os.path.isdir(module_dir))

            if os.path.isdir(module_dir) and os.listdir(module_dir):
                # self.module_exists = True
                # self.set_result(
                #     self.check_id, self.check_name, self.module_exists == True
                # )
                # if self.module_denied is None:
                self.check_deny(global_config=global_config)
                # if (
                #     moddir
                #     == f"/lib/modules/{os.uname().release}/kernel/{self.module_path}"
                # ):
                self.check_loadable()
                self.check_loaded()
            else:
                logger.info(f"Module {self.module_name} does not exist in {module_dir}")
                self.module_exists = False
                # self.set_result(
                #     self.check_id, self.check_name, self.module_exists == False
                # )
