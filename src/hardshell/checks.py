from src.hardshell.linux import (
    check_module,
    # check_mount_options,
    # check_mount_point,
    # check_package,
    # check_parameter,
    check_path,
    check_service,
)


class SystemCheck:
    def __init__(
        self,
        check_id=None,
        check_name=None,
        check_type=None,
        check_path=None,
        expected_gid=None,
        expected_permissions=None,
        expected_uid=None,
        path_exists=None,
        instance_type=None,
        module_name=None,
        module_type=None,
        module_blacklisted=None,
        module_denied=None,
        module_loadable=None,
        module_loaded=None,
        package_name=None,
        package_status=None,
        parameter_type=None,
        service_name=None,
        service_active=None,
        service_enabled=None,
        service_masked=None,
        valid_os=None,
    ):
        self.check_id = check_id
        self.check_name = check_name
        self.check_path = check_path
        self.check_result = None
        self.check_results = []
        self.check_type = check_type
        self.expected_gid = expected_gid
        self.expected_permissions = expected_permissions
        self.expected_uid = expected_uid
        self.path_exists = path_exists
        self.instance_type = instance_type
        self.module_name = module_name
        self.module_type = module_type
        self.module_blacklisted = module_blacklisted
        self.module_denied = module_denied
        self.module_loadable = module_loadable
        self.module_loaded = module_loaded
        self.package_name = package_name
        self.package_status = package_status
        self.parameter_type = parameter_type
        self.service_name = service_name
        self.service_active = service_active
        self.service_enabled = service_enabled
        self.service_masked = service_masked
        self.valid_os = valid_os

    def run_check(self, current_os, global_config):
        os_version = current_os["id"] + "-" + current_os["version_id"]
        if self.valid_os != None and os_version in self.valid_os:
            if current_os["type"] == "linux":
                # print(self.check_name)
                if self.check_type == "path":
                    # FINISHED
                    # check_path(self)
                    pass
                elif self.check_type == "module":
                    check_module(self)
                    # pass
                elif self.check_type == "mount-options":
                    # check_mount_options(self)
                    pass
                elif self.check_type == "mount-point":
                    # check_mount_point(self)
                    pass
                elif self.check_type == "package":
                    # check_package(self)
                    pass
                elif self.check_type == "parameter":
                    # check_parameter(self)
                    pass
                elif self.check_type == "service":
                    # FINISHED
                    # check_service(self)
                    pass
            else:
                print("Check Not Supported")
        else:
            pass
            # self.check_result = "Invalid OS"

    def get_results(self):
        return self.check_results

    def set_result(self, result):
        self.check_results.append(result)

    def set_service_active_result(self, result):
        self.result_service_active = result

    def set_service_enabled_result(self, result):
        self.result_service_enabled = result
