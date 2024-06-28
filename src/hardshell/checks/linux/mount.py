import os
import subprocess
from dataclasses import dataclass, field
from typing import List

import psutil

from src.hardshell.checks.base import BaseCheck


@dataclass
class MountCheck(BaseCheck):
    mount_boot: bool = False
    mount_exists: bool = False
    mount_options: List[str] = field(default_factory=list)
    path: str = None
    separate_partition: bool = False

    def check_mount_boot(self, mount_point):
        """Check if a mount point gets mounted at boot by looking at /etc/fstab."""
        try:
            with open("/etc/fstab", "r") as fstab:
                for line in fstab:
                    if mount_point in line and not line.strip().startswith("#"):
                        return True
            return False
        except Exception as e:
            print(f"Error reading /etc/fstab: {e}")
            return False

    def check_mount_exists(self, mount_point):
        """Check if a mount point exists."""
        return os.path.ismount(mount_point)

    # TODO Fix this
    def check_mount_options(self, mount_point, options):
        """Check if specific mount options are set for the mount point."""
        try:
            with open("/proc/mounts", "r") as mounts:
                for line in mounts:
                    parts = line.split()
                    if parts[1] == mount_point:
                        mount_options = parts[3].split(",")
                        for option in options:
                            if option not in mount_options:
                                return False, option
                        return True, None
            return False, None
        except Exception as e:
            print(f"Error checking mount options: {e}")
            return False, None

    def check_mount_partition(self, mount_point):
        """Check if a mount point is a separate partition."""
        try:
            for part in psutil.disk_partitions(all=True):
                if part.mountpoint == mount_point:
                    if part.fstype != "tmpfs" and "overlay" not in part.device:
                        return True
            return False
        except Exception as e:
            print(f"Error checking partition: {e}")
            return False

    def is_mounted(self, mount_point):
        """Check if the mount point is currently mounted."""
        try:
            output = (
                subprocess.check_output(["mount"]).decode("utf-8").strip().split("\n")
            )
            for line in output:
                if mount_point in line:
                    return True
            return False
        except subprocess.CalledProcessError as e:
            print(f"Error checking current mounts: {e}")
            return False

    def run_check(self, current_os, global_config):
        self.set_result_and_log_status(
            log_message=f"checking mount {self.path}", log_only=True
        )

        # check if a mount point exists
        mount_exists = self.check_mount_exists(self.path)
        self.set_result_and_log_status(
            check_id=self.check_id,
            check_message="mount exists",
            check_name=self.check_name,
            check_result="pass" if mount_exists == self.mount_exists else "fail",
            check_type=self.check_type,
            log_message=f"mount {self.path} exists: {mount_exists}",
        )

        if mount_exists:
            # check if the mount is mounted
            is_mounted = self.is_mounted(self.path)
            self.set_result_and_log_status(
                check_id=self.check_id,
                check_message="mount is mounted",
                check_name=self.check_name,
                check_result="pass" if is_mounted else "fail",
                check_type=self.check_type,
                log_message=f"mount {self.path} is mounted: {is_mounted}",
            )
            if is_mounted:
                # check mount options
                mount_options = self.check_mount_options(self.path, self.mount_options)
                self.set_result_and_log_status(
                    check_id=self.check_id,
                    check_message="mount options",
                    check_name=self.check_name,
                    check_result="pass" if mount_options else "fail",
                    check_type=self.check_type,
                    log_message=f"mount {self.path} options configured: {mount_options}",
                )

                # check if the mount is a separate partition
                separate_partition = self.check_mount_partition(self.path)
                self.set_result_and_log_status(
                    check_id=self.check_id,
                    check_message="mount is separate partition",
                    check_name=self.check_name,
                    check_result="pass"
                    if separate_partition == self.separate_partition
                    else "fail",
                    check_type=self.check_type,
                    log_message=f"mount {self.path} is separate partition: {separate_partition}",
                )

                # check if the mount is mounted at boot
                mount_boot = self.check_mount_boot(self.path)
                self.set_result_and_log_status(
                    check_id=self.check_id,
                    check_message="mount is mounted at boot",
                    check_name=self.check_name,
                    check_result="pass" if mount_boot == self.mount_boot else "fail",
                    check_type=self.check_type,
                    log_message=f"mount {self.path} is mounted at boot: {mount_boot}",
                )
        else:
            # Mount is Mounted
            self.set_result_and_log_status(
                check_id=self.check_id,
                check_message="mount is mounted",
                check_name=self.check_name,
                check_result="skip",
                check_type=self.check_type,
                log_message=f"mount {self.path} is mounted check skipped",
            )

            # Mount Options
            self.set_result_and_log_status(
                check_id=self.check_id,
                check_message="mount options",
                check_name=self.check_name,
                check_result="skip",
                check_type=self.check_type,
                log_message=f"mount {self.path} options check skipped",
            )

            # Separate Partition
            self.set_result_and_log_status(
                check_id=self.check_id,
                check_message="mount separate partition",
                check_name=self.check_name,
                check_result="skip",
                check_type=self.check_type,
                log_message=f"mount {self.path} separate partition check skipped",
            )

            # Mount at Boot
            self.set_result_and_log_status(
                check_id=self.check_id,
                check_message="mount is mounted at boot",
                check_name=self.check_name,
                check_result="skip",
                check_type=self.check_type,
                log_message=f"mount {self.path} is mounted at boot check skipped",
            )
