from dataclasses import dataclass, field
from typing import List
from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.logging import logger
from pystemd.systemd1 import Manager, Unit


@dataclass
class ServiceCheck(BaseCheck):
    path: str = None
    path_exists: bool = False
    permissions: List[int] = field(default_factory=list)
    recursive: bool = False

    def run_check(self, current_os, global_config):
        print("Running service check")

        manager = Manager()

        manager.load()

        result = manager.Manager.ListUnitFiles()

        print(result)

        # stopped = manager.Manager.StopUnit("cron.service", "replace")

        # print(stopped)

        # started = manager.Manager.StartUnit("cron.service", "replace")

        # print(started)
