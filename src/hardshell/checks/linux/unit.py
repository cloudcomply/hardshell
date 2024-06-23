import os
from dataclasses import dataclass, field
from typing import List
from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.logging import logger
import pystemd
from pystemd.systemd1 import Manager, Unit


@dataclass
class UnitCheck(BaseCheck):
    unit_active: bool = False  # active | inactive # checked with ActiveState
    unit_loaded: bool = False  # loaded | masked | not-found # checked with LoadState
    unit_name: str = None
    unit_state: str = "masked"  # disabled | enabled | enabled-runtime | masked # checked with UnitFileState

    def log_and_print(self, message, level="info"):
        print(message)
        getattr(logger, level)(message)

    def check_unit_state(self, unit_name, expected_state, actual_state, state_type):
        if actual_state == expected_state:
            self.log_and_print(
                f"Unit {unit_name} is {actual_state} and supposed to be {expected_state}."
            )
        else:
            self.log_and_print(
                f"Unit {unit_name} is {actual_state} and supposed to be {expected_state}.",
                level="error",
            )

    def run_check(self, current_os, global_config):
        print("Running unit check")
        try:
            manager = Manager()
            manager.load()

            unit_exists = manager.GetUnit(self.unit_name.encode("utf-8"))
            unit_exists_decoded = unit_exists.decode("utf-8")

            self.log_and_print(f"Unit Exists: {unit_exists_decoded}")

            if unit_exists and os.path.exists(
                f"/usr/lib/systemd/system/{self.unit_name}"
            ):
                self.log_and_print(f"Unit {self.unit_name} exists")

                unit = Unit(self.unit_name.encode("utf-8"))
                unit.load()

                active_state = unit.ActiveState.decode("utf-8")
                load_state = unit.LoadState.decode("utf-8")
                unit_file_state = unit.UnitFileState.decode("utf-8")

                if load_state == "not-found":
                    self.log_and_print(
                        f"Unit {self.unit_name} does not exist.", level="error"
                    )
                    return

                self.check_unit_state(
                    self.unit_name,
                    "active" if self.unit_active else "inactive",
                    active_state,
                    "ActiveState",
                )
                self.check_unit_state(
                    self.unit_name,
                    "loaded" if self.unit_loaded else "not loaded",
                    load_state,
                    "LoadState",
                )
                self.check_unit_state(
                    self.unit_name, self.unit_state, unit_file_state, "UnitFileState"
                )
            else:
                self.log_and_print(f"Unit {self.unit_name} does not exist")

        except pystemd.dbusexc.DBusNoSuchUnitError as e:
            self.log_and_print(f"Unit {self.unit_name} does not exist", level="error")
            logger.error(e)
