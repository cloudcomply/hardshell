from src.hardshell.checks import SystemCheck


def create_checks(config):
    checks = []
    for system_check in config:
        for check in config[system_check]:
            new_check = SystemCheck(
                check_id=check,
                check_name=config[system_check][check].get("check_name"),
                check_type=config[system_check][check]["check_type"],
                valid_os=config[system_check][check].get("valid_os"),
                check_path=config[system_check][check].get("check_path"),
                expected_gid=config[system_check][check].get("expected_gid"),
                expected_permissions=config[system_check][check].get(
                    "expected_permissions"
                ),
                expected_uid=config[system_check][check].get("expected_uid"),
                path_exists=config[system_check][check].get("path_exists"),
                instance_type=config[system_check][check].get("instance_type"),
                module_name=config[system_check][check].get("module_name"),
                module_type=config[system_check][check].get("module_type"),
                module_blacklisted=config[system_check][check].get("module_blacklisted"),
                module_denied=config[system_check][check].get("module_denied"),
                module_loadable=config[system_check][check].get("module_loadable"),
                module_loaded=config[system_check][check].get("module_loaded"),
                package_name=config[system_check][check].get("package_name"),
                package_status=config[system_check][check].get("package_status"),
                parameter_type=config[system_check][check].get("parameter_type"),
                service_name=config[system_check][check].get("service_name"),
                service_active=config[system_check][check].get("service_active"),
                service_enabled=config[system_check][check].get("service_enabled"),
                service_masked=config[system_check][check].get("service_masked"),
            )
            checks.append(new_check)
    return checks
