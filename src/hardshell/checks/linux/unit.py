import os
import platform
from dataclasses import dataclass, field
from typing import List

if platform.system() == "Linux":
    import pystemd
    from pystemd.systemd1 import Manager, Unit

from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.common import log_and_print


@dataclass
class UnitCheck(BaseCheck):
    unit_active: bool = False  # active | inactive
    unit_loaded: bool = False  # loaded | masked | not-found
    unit_name: str = None
    unit_state: str = "masked"  # disabled | enabled | enabled-runtime | masked

    def check_unit_state(self, unit_name, expected_state, actual_state, state_type):
        if actual_state == expected_state:
            log_and_print(
                f"Unit {unit_name} is {actual_state} and supposed to be {expected_state}.",
                # log_only=True,
            )
            return True
        else:
            log_and_print(
                f"Unit {unit_name} is {actual_state} and supposed to be {expected_state}.",
                level="error",
                # log_only=True,
            )
            return False

    def run_check(self, current_os, global_config):
        log_and_print("running unit check", log_only=True)
        self.run_check_systemd()

    def run_check_systemd(self):
        log_and_print(
            f"running unit check for systemd for {self.unit_name}", log_only=True
        )
        try:
            manager = Manager()
            manager.load()

            unit_exists = manager.GetUnit(self.unit_name.encode("utf-8"))
            unit_exists_decoded = unit_exists.decode("utf-8")

            log_and_print(f"unit exists: {unit_exists_decoded}", log_only=True)

            if unit_exists and os.path.exists(
                f"/usr/lib/systemd/system/{self.unit_name}"
            ):
                log_and_print(f"unit {self.unit_name} exists", log_only=True)

                unit = Unit(self.unit_name.encode("utf-8"))
                unit.load()

                active_state = unit.ActiveState.decode("utf-8")
                load_state = unit.LoadState.decode("utf-8")
                unit_file_state = unit.UnitFileState.decode("utf-8")

                if load_state == "not-found":
                    log_and_print(
                        f"unit {self.unit_name} not found.",
                        level="error",
                        log_only=True,
                    )
                    return

                active_status = self.check_unit_state(
                    self.unit_name,
                    "active" if self.unit_active else "inactive",
                    active_state,
                    "ActiveState",
                )
                loaded_status = self.check_unit_state(
                    self.unit_name,
                    # "loaded" if self.unit_loaded else "not loaded",
                    "loaded" if self.unit_loaded else "masked",
                    load_state,
                    "LoadState",
                )
                unit_file_status = self.check_unit_state(
                    self.unit_name, self.unit_state, unit_file_state, "UnitFileState"
                )

                print(active_state == active_status)
                print(load_state == loaded_status)
                print(unit_file_state == unit_file_status)

                # self.set_result_and_log_status(
                #     self.check_id,
                #     self.check_name,
                #     "pass"
                #     if active_state == active_status
                #     and load_state == loaded_status
                #     and unit_file_state == unit_file_status
                #     else "fail",
                #     "service status",
                #     self.check_type,
                # )
            else:
                log_and_print(f"unit {self.unit_name} does not exist", log_only=True)

            self.set_result_and_log_status(
                self.check_id,
                self.check_name,
                "pass"
                if active_status and loaded_status and unit_file_status
                else "fail",
                "service status",
                self.check_type,
            )

        except AttributeError as e:
            log_and_print(
                f"unit {self.unit_name} does not exist: {e}",
                level="error",
                log_only=True,
            )
        except pystemd.dbusexc.DBusFileNotFoundError as e:
            log_and_print(
                f"unit {self.unit_name} does not exist: {e}",
                level="error",
                log_only=True,
            )
        except pystemd.dbusexc.DBusNoSuchUnitError as e:
            log_and_print(
                f"unit {self.unit_name} does not exist: {e}",
                level="error",
                log_only=True,
            )
