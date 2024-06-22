from src.hardshell.checks.system import SystemCheck
from src.hardshell.checks.linux.module import ModuleCheck
from src.hardshell.checks.linux.mount import MountCheck
from src.hardshell.checks.linux.package import PackageCheck
from src.hardshell.checks.linux.path import PathCheck
from src.hardshell.checks.linux.regex import RegexCheck
from src.hardshell.checks.linux.service import ServiceCheck
from src.hardshell.common.logging import logger


def create_checks(config):
    checks = []
    for system_check in config:
        for check in config[system_check]:
            if not config[system_check][check].get("check_skip"):
                category = config[system_check][check].get("category")
                check_id = check
                check_name = config[system_check][check].get("check_name")
                check_subtype = config[system_check][check].get("check_subtype", None)
                check_type = config[system_check][check].get("check_type")
                depends_on = config[system_check][check].get("depends_on")
                valid_os = config[system_check][check].get("valid_os", [])

                if config[system_check][check].get("check_type") == "module":
                    # logger.info(
                    #     f"Creating Check: {config[system_check][check].get('check_name')}"
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
                    # logger.info(
                    #     f"Creating Check: {config[system_check][check].get('check_name')}"
                    # )
                    # new_check = ModuleCheck(
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
                elif config[system_check][check].get("check_type") == "package":
                    # logger.info(
                    #     f"Creating Check: {config[system_check][check].get('check_name')}"
                    # )
                    # new_check = PackageCheck(
                    #     category=category,
                    #     check_id=check_id,
                    #     check_name=check_name,
                    #     check_subtype=check_subtype,
                    #     check_type=check_type,
                    #     depends_on=depends_on,
                    #     package_name=config[system_check][check].get("package_name"),
                    #     package_installed=config[system_check][check].get(
                    #         "package_installed"
                    #     ),
                    #     valid_os=valid_os,
                    # )
                    # checks.append(new_check)
                    pass
                elif config[system_check][check].get("check_type") == "path":
                    # logger.info(
                    #     f"Creating Check: {config[system_check][check].get('check_name')}"
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
                    # logger.info(
                    #     f"Creating Check: {config[system_check][check].get('check_name')}"
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
                elif config[system_check][check].get("check_type") == "service":
                    logger.info(
                        f"Creating Check: {config[system_check][check].get('check_name')}"
                    )
                    new_check = ServiceCheck(
                        category=category,
                        check_id=check_id,
                        check_name=check_name,
                        check_subtype=check_subtype,
                        check_type=check_type,
                        depends_on=depends_on,
                        valid_os=valid_os,
                    )
                    checks.append(new_check)
                    pass
                else:
                    pass
            else:
                logger.info(
                    f"Skipping Check: {config[system_check][check].get('check_name')}"
                )
    return checks
