from dataclasses import dataclass, field
from typing import List, Optional
from src.hardshell.linux import (
    check_module,
    check_mount,
    check_package,
    check_parameter,
    check_path,
    check_service,
)


@dataclass
class SystemCheck:
    check_id: Optional[str] = None
    check_name: Optional[str] = None
    check_type: Optional[str] = None
    expected_gid: Optional[int] = None
    expected_permissions: Optional[int] = None
    expected_uid: Optional[int] = None
    path_exists: Optional[bool] = None
    instance_type: Optional[str] = None
    module_name: Optional[str] = None
    module_type: Optional[str] = None
    module_blacklisted: Optional[bool] = None
    module_denied: Optional[bool] = None
    module_loadable: Optional[bool] = None
    module_loaded: Optional[bool] = None
    mount_exists: Optional[bool] = None
    nodev: Optional[bool] = None
    noexec: Optional[bool] = None
    nosuid: Optional[bool] = None
    package_name: Optional[str] = None
    package_install: Optional[str] = None
    parameter: Optional[str] = None
    path: Optional[str] = None
    separate_partition: Optional[bool] = None
    service_name: Optional[str] = None
    service_active: Optional[bool] = None
    service_enabled: Optional[bool] = None
    service_masked: Optional[bool] = None
    valid_os: Optional[List[str]] = field(default_factory=list)
    check_result: Optional[str] = None
    check_results: List[str] = field(default_factory=list)

    def run_check(self, current_os, global_config):
        os_version = current_os["id"] + "-" + current_os["version_id"]
        if self.valid_os != None and os_version in self.valid_os:
            if current_os["type"] == "linux":
                # print(self.check_name)
                if self.check_type == "module":
                    # FINISHED
                    check_module(self)
                    # pass
                elif self.check_type == "mount":
                    # FINISHED
                    check_mount(self)
                    # pass
                elif self.check_type == "package":
                    check_package(self, current_os, global_config)
                    # pass
                elif self.check_type == "parameter":
                    # FINISHED
                    check_parameter(self, global_config)
                    # pass
                elif self.check_type == "path":
                    # FINISHED
                    check_path(self)
                    # pass
                elif self.check_type == "service":
                    # FINISHED
                    check_service(self)
                    # pass
            else:
                print("Check Not Supported")
        else:
            # self.check_result = "Invalid OS"
            pass

    def get_results(self):
        return self.check_results

    def set_result(self, result):
        self.check_results.append(result)
