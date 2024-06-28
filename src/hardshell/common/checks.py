from src.hardshell.checks.linux.accounts import AccountsCheck
from src.hardshell.checks.linux.module import ModuleCheck
from src.hardshell.checks.linux.mount import MountCheck
from src.hardshell.checks.linux.package import PackageCheck
from src.hardshell.checks.linux.path import PathCheck
from src.hardshell.checks.linux.regex import RegexCheck
from src.hardshell.checks.linux.unit import UnitCheck
from src.hardshell.common.common import log_and_print

CHECK_CLASSES = {
    "accounts": AccountsCheck,
    "module": ModuleCheck,
    "mount": MountCheck,
    "package": PackageCheck,
    "path": PathCheck,
    "regex": RegexCheck,
    "unit": UnitCheck,
}


def create_check_instance(check_type, params):
    check_class = CHECK_CLASSES.get(check_type)
    if check_class:
        log_and_print(f"creating check: {params.get('check_name')}", log_only=True)
        return check_class(**params)
    return None


def create_checks(config, current_os):
    checks = []
    os_version = f"{current_os['id']}-{current_os['version_id']}"

    for system_check in config.values():
        for check, check_config in system_check.items():
            if check_config.get("check_skip") or os_version not in check_config.get(
                "valid_os", []
            ):
                continue

            common_params = {
                "category": check_config.get("category"),
                "check_id": f"{check_config.get('category', 'custom')}-{check}",
                "check_name": check_config.get("check_name"),
                "check_subtype": check_config.get("check_subtype", None),
                "check_type": check_config.get("check_type"),
                "depends_on": check_config.get("depends_on", []),
                "valid_os": check_config.get("valid_os", []),
            }

            specific_params = {}
            if check_config["check_type"] == "module":
                specific_params = {
                    "module_denied": check_config.get("module_denied"),
                    "module_exists": check_config.get("module_exists"),
                    "module_loadable": check_config.get("module_loadable"),
                    "module_loaded": check_config.get("module_loaded"),
                    "module_name": check_config.get("module_name"),
                    "module_path": check_config.get("module_path"),
                }
            elif check_config["check_type"] == "mount":
                specific_params = {
                    "mount_boot": check_config.get("mount_boot"),
                    "mount_exists": check_config.get("mount_exists"),
                    "mount_options": check_config.get("mount_options"),
                    "path": check_config.get("path"),
                    "separate_partition": check_config.get("separate_partition"),
                }
            elif check_config["check_type"] == "package":
                specific_params = {
                    "package_name": check_config.get("package_name"),
                    "package_installed": check_config.get("package_installed"),
                }
            elif check_config["check_type"] == "path":
                specific_params = {
                    "path": check_config.get("path"),
                    "path_exists": check_config.get("path_exists"),
                    "permissions": check_config.get("permissions"),
                    "recursive": check_config.get("recursive", False),
                }
            elif check_config["check_type"] == "regex":
                specific_params = {
                    "file_ext": check_config.get("file_ext", None),
                    "ignore_case": check_config.get("ignore_case", False),
                    "multi_line": check_config.get("multi_line", False),
                    "path": check_config.get("path"),
                    "pattern": check_config.get("pattern"),
                    "pattern_match": check_config.get("pattern_match", False),
                }
            elif check_config["check_type"] == "unit":
                specific_params = {
                    "unit_active": check_config.get("unit_active"),
                    "unit_loaded": check_config.get("unit_loaded"),
                    "unit_name": check_config.get("unit_name"),
                    "unit_state": check_config.get("unit_state"),
                }

            # print(f"Check: {check_config.get('check_name')}")
            check_instance = create_check_instance(
                check_config["check_type"], {**common_params, **specific_params}
            )
            if check_instance:
                checks.append(check_instance)

    return checks
