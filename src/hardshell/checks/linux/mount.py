from dataclasses import dataclass, field
from typing import List

from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.logging import logger


@dataclass
class MountCheck(BaseCheck):
    mount_exists: bool = False
    path: str = None
    # permissions: List[int] = field(default_factory=list)
    # recursive: bool = False

    def run_check(self, current_os, global_config):
        pass
