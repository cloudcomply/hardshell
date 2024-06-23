from dataclasses import dataclass, field
from typing import List, Optional

# from src.hardshell.linux import (  # check_test,
#     check_accounts,
#     check_command,
#     check_module,
#     check_mount,
#     check_package,
#     check_path,
#     check_regex,
#     check_service,
#     check_ssh_keys,
#     check_unconfined_services,
# )


@dataclass
class SystemCheck:
    category: Optional[str] = None
    check_files: Optional[bool] = None
    check_id: Optional[str] = None
    check_name: Optional[str] = None
    check_results: List[str] = field(default_factory=list)
    check_subtype: Optional[str] = None
    check_type: Optional[str] = None
    command: Optional[str] = None
    depends_on: Optional[List[str]] = field(default_factory=list)
    expected_gid: Optional[int] = None
    expected_output: Optional[str] = None
    expected_permissions: Optional[int] = None
    expected_perms: Optional[int] = None
    expected_uid: Optional[int] = None
    field_match: Optional[str] = None
    field_value: Optional[str] = None
    file_extension: Optional[str] = None
    # module_name: Optional[str] = None
    # module_blacklisted: Optional[bool] = None
    # module_denied: Optional[bool] = None
    # module_loadable: Optional[bool] = None
    # module_loaded: Optional[bool] = None
    mount_boot: Optional[bool] = None
    mount_exists: Optional[bool] = None
    nodev: Optional[bool] = None
    noexec: Optional[bool] = None
    nosuid: Optional[bool] = None
    # package_name: Optional[str] = None
    # package_install: Optional[str] = None
    parameter: Optional[str] = None
    path: Optional[str] = None
    path_exists: Optional[bool] = None
    pattern: Optional[str] = None
    pattern_exists: Optional[bool] = True
    separate_partition: Optional[bool] = None
    service_name: Optional[str] = None
    service_active: Optional[bool] = None
    service_enabled: Optional[bool] = None
    service_masked: Optional[bool] = None
    valid_os: Optional[List[str]] = field(default_factory=list)

    def run_check(self, current_os, global_config):
        os_version = current_os["id"] + "-" + current_os["version_id"]
        if self.valid_os != None and os_version in self.valid_os:
            if current_os["type"] == "linux":
                # print(f"Running Check: {self.check_name}")
                # print(f"Check Type: {self.check_type}")
                if self.check_type == "accounts":
                    # print(self.check_name)
                    # check_accounts(self)
                    pass
                elif self.check_type == "command":
                    # print(self.check_name)
                    # check_command(self)
                    pass
                # elif self.check_type == "kernel-module":
                #     # print(self.check_name)
                #     # check_module(self)
                #     pass
                elif self.check_type == "mount":
                    # print(self.check_name)
                    # check_mount(self)
                    pass
                elif self.check_type == "package":
                    # print(self.check_name)
                    # check_package(self, current_os, global_config)
                    pass
                elif self.check_type == "path":
                    # print(self.check_name)
                    # check_path(self)
                    pass
                elif self.check_type == "regex":
                    # print(self.check_name)
                    # check_regex(self, global_config)
                    pass
                elif self.check_type == "service":
                    # print(self.check_name)
                    # check_service(self)
                    pass
                elif self.check_type == "ssh-keys":
                    # print(self.check_name)
                    # check_ssh_keys(self)
                    pass
                elif self.check_type == "test":
                    # print(self.check_name)
                    # check_test(self)
                    pass
                elif self.check_type == "unconfined-services":
                    # print(self.check_name)
                    # check_unconfined_services(self)
                    pass
            else:
                print("Check Not Supported")
        else:
            # self.check_result = "Invalid OS"
            pass

    def get_results(self):
        return self.check_results

    def set_result(self, result):
        self.check_results.append(result)
