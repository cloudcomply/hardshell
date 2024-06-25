from src.hardshell.checks.linux.accounts import AccountsCheck
from src.hardshell.checks.linux.module import ModuleCheck
from src.hardshell.checks.linux.mount import MountCheck
from src.hardshell.checks.linux.package import PackageCheck
from src.hardshell.checks.linux.path import PathCheck
from src.hardshell.checks.linux.regex import RegexCheck
from src.hardshell.checks.linux.unit import UnitCheck
from src.hardshell.common.common import log_and_print


def create_checks(config, current_os):
    checks = []
    for system_check in config:
        for check in config[system_check]:
            if not config[system_check][check].get(
                "check_skip"
            ) and f"{current_os['id']}-{current_os['version_id']}" in config[
                system_check
            ][
                check
            ].get(
                "valid_os", []
            ):
                category = config[system_check][check].get("category")
                check_id = (
                    config[system_check][check].get("category", "custom") + "-" + check
                )
                check_name = config[system_check][check].get("check_name")
                check_subtype = config[system_check][check].get("check_subtype", None)
                check_type = config[system_check][check].get("check_type")
                depends_on = config[system_check][check].get("depends_on")
                valid_os = config[system_check][check].get("valid_os", [])

                if config[system_check][check].get("check_type") == "accounts":
                    # log_and_print(
                    #     f"creating check: {config[system_check][check].get('check_name')}",
                    #     log_only=True,
                    # )
                    # new_check = AccountsCheck(
                    #     category=category,
                    #     check_id=check_id,
                    #     check_name=check_name,
                    #     check_subtype=check_subtype,
                    #     check_type=check_type,
                    #     depends_on=depends_on,
                    #     valid_os=valid_os,
                    # )
                    # checks.append(new_check)
                    pass
                elif config[system_check][check].get("check_type") == "module":
                    # log_and_print(
                    #     f"creating check: {config[system_check][check].get('check_name')}",
                    #     log_only=True,
                    # )
                    # new_check = ModuleCheck(
                    #     category=category,
                    #     check_id=check_id,
                    #     check_name=check_name,
                    #     check_subtype=check_subtype,
                    #     check_type=check_type,
                    #     depends_on=depends_on,
                    #     module_denied=config[system_check][check].get("module_denied"),
                    #     module_exists=config[system_check][check].get("module_exists"),
                    #     module_loadable=config[system_check][check].get(
                    #         "module_loadable"
                    #     ),
                    #     module_loaded=config[system_check][check].get("module_loaded"),
                    #     module_name=config[system_check][check].get("module_name"),
                    #     module_path=config[system_check][check].get("module_path"),
                    #     valid_os=valid_os,
                    # )
                    # checks.append(new_check)
                    pass
                elif config[system_check][check].get("check_type") == "mount":
                    # log_and_print(
                    #     f"creating check: {config[system_check][check].get('check_name')}",
                    #     log_only=True,
                    # )
                    # new_check = MountCheck(
                    #     category=category,
                    #     check_id=check_id,
                    #     check_name=check_name,
                    #     check_subtype=check_subtype,
                    #     check_type=check_type,
                    #     depends_on=depends_on,
                    #     mount_boot=config[system_check][check].get("mount_boot"),
                    #     mount_exists=config[system_check][check].get("mount_exists"),
                    #     mount_options=config[system_check][check].get("mount_options"),
                    #     path=config[system_check][check].get("path"),
                    #     separate_partition=config[system_check][check].get(
                    #         "separate_partition"
                    #     ),
                    #     valid_os=valid_os,
                    # )
                    # checks.append(new_check)
                    pass
                elif config[system_check][check].get("check_type") == "package":
                    log_and_print(
                        f"creating check: {config[system_check][check].get('check_name')}",
                        log_only=True,
                    )
                    new_check = PackageCheck(
                        category=category,
                        check_id=check_id,
                        check_name=check_name,
                        check_subtype=check_subtype,
                        check_type=check_type,
                        depends_on=depends_on,
                        package_name=config[system_check][check].get("package_name"),
                        package_installed=config[system_check][check].get(
                            "package_installed"
                        ),
                        valid_os=valid_os,
                    )
                    checks.append(new_check)
                    pass
                elif config[system_check][check].get("check_type") == "path":
                    # log_and_print(
                    #     f"creating check: {config[system_check][check].get('check_name')}",
                    #     log_only=True,
                    # )
                    # new_check = PathCheck(
                    #     category=category,
                    #     check_id=check_id,
                    #     check_name=check_name,
                    #     check_subtype=check_subtype,
                    #     check_type=check_type,
                    #     depends_on=depends_on,
                    #     path=config[system_check][check].get("path"),
                    #     path_exists=config[system_check][check].get("path_exists"),
                    #     permissions=config[system_check][check].get("permissions"),
                    #     recursive=config[system_check][check].get("recursive", False),
                    #     valid_os=valid_os,
                    # )
                    # checks.append(new_check)
                    pass
                elif config[system_check][check].get("check_type") == "regex":
                    # log_and_print(
                    #     f"creating check: {config[system_check][check].get('check_name')}",
                    #     log_only=True,
                    # )
                    # new_check = RegexCheck(
                    #     category=category,
                    #     check_id=check_id,
                    #     check_name=check_name,
                    #     check_subtype=check_subtype,
                    #     check_type=check_type,
                    #     depends_on=depends_on,
                    #     file_ext=config[system_check][check].get("file_ext", None),
                    #     ignore_case=config[system_check][check].get(
                    #         "ignore_case", False
                    #     ),
                    #     multi_line=config[system_check][check].get("multi_line", False),
                    #     path=config[system_check][check].get("path"),
                    #     pattern=config[system_check][check].get("pattern"),
                    #     pattern_match=config[system_check][check].get(
                    #         "pattern_match", False
                    #     ),
                    #     valid_os=valid_os,
                    # )
                    # checks.append(new_check)
                    pass
                elif config[system_check][check].get("check_type") == "unit":
                    # log_and_print(
                    #     f"creating check: {config[system_check][check].get('check_name')}",
                    #     log_only=True,
                    # )
                    # new_check = UnitCheck(
                    #     category=category,
                    #     check_id=check_id,
                    #     check_name=check_name,
                    #     check_subtype=check_subtype,
                    #     check_type=check_type,
                    #     depends_on=depends_on,
                    #     unit_active=config[system_check][check].get("unit_active"),
                    #     unit_loaded=config[system_check][check].get("unit_loaded"),
                    #     unit_name=config[system_check][check].get("unit_name"),
                    #     unit_state=config[system_check][check].get("unit_state"),
                    #     valid_os=valid_os,
                    # )
                    # checks.append(new_check)
                    pass
                else:
                    pass
            else:
                # log_and_print(
                #     f"creating check: {config[system_check][check].get('check_name')}",
                #     log_only=True,
                # )
                pass
    return checks
