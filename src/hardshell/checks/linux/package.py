import glob
import os
import re
from dataclasses import dataclass
from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.logging import logger


@dataclass
class PackageCheck(BaseCheck):
    package_name: str = None
    package_installed: bool = False

    def run_check(self, current_os, global_config):
        logger.info(f"Checking package {self.package_name}")
        print("Running Package Check")
        print(f"Package Name: {self.package_name}")
        pass
