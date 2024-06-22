import glob
import os
from dataclasses import dataclass, field
from typing import List
from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.logging import logger


@dataclass
class PathCheck(BaseCheck):
    path: str = None
    path_exists: bool = False
    permissions: List[int] = field(default_factory=list)
    recursive: bool = False

    def check_path(self, path):
        logger.info(f"Checking path: {path}")
        stats = self.get_permissions(path)
        current_permissions = (stats.st_uid, stats.st_gid, int(oct(stats.st_mode)[-3:]))

        if current_permissions == self.permissions:
            logger.info(f"Path {path} has the expected permissions: {self.permissions}")
            result = "pass"
        else:
            logger.warning(
                f"Path {path} does not have the expected permissions: {self.permissions}"
            )
            result = "fail"

        self.set_result(
            self.check_id, self.check_name, result, "permissions", self.check_type
        )

    def get_permissions(self, path):
        return os.stat(path)

    def run_check(self, current_os, global_config):
        logger.info(f"Checking path: {self.path}")
        path_exists = os.path.exists(self.path)

        if path_exists:
            logger.info(
                f"Path {self.path} exists and is expected to exist: {self.path_exists}"
            )
            result = "pass" if self.path_exists else "fail"
        else:
            logger.info(
                f"Path {self.path} does not exist and is expected to exist: {self.path_exists}"
            )
            result = "pass" if not self.path_exists else "fail"

        self.set_result(
            self.check_id, self.check_name, result, "exists", self.check_type
        )

        if path_exists:
            self.check_path(self.path)
            if os.path.isdir(self.path) and self.recursive:
                for new_path in glob.glob(
                    os.path.join(self.path, "**", "*"), recursive=True
                ):
                    self.check_path(new_path)
