from src.hardshell.checks import SystemCheck


def create_checks(config):
    checks = []
    for system_check in config:
        for check in config[system_check]:
            if not config[system_check][check].get("check_skip"):
                new_check = SystemCheck(
                    category=config[system_check][check].get("category"),
                    check_files=config[system_check][check].get("check_files"),
                    check_id=check,
                    check_name=config[system_check][check].get("check_name"),
                    check_type=config[system_check][check].get("check_type"),
                    command=config[system_check][check].get("command"),
                    depends_on=config[system_check][check].get("depends_on"),
                    expected_gid=config[system_check][check].get(
                        "expected_gid"
                    ),
                    expected_output=config[system_check][check].get(
                        "expected_output"
                    ),
                    expected_permissions=config[system_check][check].get(
                        "expected_permissions"
                    ),
                    expected_perms=config[system_check][check].get(
                        "expected_perms"
                    ),
                    expected_uid=config[system_check][check].get(
                        "expected_uid"
                    ),
                    field_match=config[system_check][check].get("field_match"),
                    field_value=config[system_check][check].get(
                        "field_value", ""
                    ),
                    file_extension=config[system_check][check].get(
                        "file_extension", ""
                    ),
                    module_name=config[system_check][check].get(
                        "module_name", ""
                    ),
                    module_blacklisted=config[system_check][check].get(
                        "module_blacklisted", True
                    ),
                    module_denied=config[system_check][check].get(
                        "module_denied", True
                    ),
                    module_loadable=config[system_check][check].get(
                        "module_loadable", False
                    ),
                    module_loaded=config[system_check][check].get(
                        "module_loaded", False
                    ),
                    mount_boot=config[system_check][check].get(
                        "mount_boot", True
                    ),
                    mount_exists=config[system_check][check].get(
                        "mount_exists", True
                    ),
                    nodev=config[system_check][check].get("nodev", False),
                    noexec=config[system_check][check].get("noexec", False),
                    nosuid=config[system_check][check].get("nosuid", False),
                    package_name=config[system_check][check].get(
                        "package_name", ""
                    ),
                    package_install=config[system_check][check].get(
                        "package_install", False
                    ),
                    parameter=config[system_check][check].get("parameter", ""),
                    path=config[system_check][check].get("path", ""),
                    path_exists=config[system_check][check].get(
                        "path_exists", True
                    ),
                    pattern=config[system_check][check].get("pattern", ""),
                    pattern_exists=config[system_check][check].get(
                        "pattern_exists", False
                    ),
                    separate_partition=config[system_check][check].get(
                        "separate_partition", True
                    ),
                    service_name=config[system_check][check].get(
                        "service_name", ""
                    ),
                    service_active=config[system_check][check].get(
                        "service_active", True
                    ),
                    service_enabled=config[system_check][check].get(
                        "service_enabled", True
                    ),
                    service_masked=config[system_check][check].get(
                        "service_masked", True
                    ),
                    valid_os=config[system_check][check].get("valid_os", []),
                )
                checks.append(new_check)
    return checks
