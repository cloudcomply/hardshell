import os
import subprocess


def check_module(check):
    def set_module_result(check, check_name, actual, expected, check_type):
        result = "PASS" if actual == expected else "FAIL"
        check.set_result({"name": check_name, "check": check_type, "result": result})

    blacklisted_check = check_module_blacklisted(check.check_name)
    denied_check = check_module_denied(check.check_name)
    loadable_check = check_module_loadable(check.check_name)
    loaded_check = check_module_loaded(check.check_name)

    set_module_result(
        check,
        check.check_name,
        blacklisted_check,
        check.module_blacklisted,
        "Module Blacklisted",
    )
    set_module_result(
        check, check.check_name, denied_check, check.module_denied, "Module Denied"
    )
    set_module_result(
        check, check.check_name, loadable_check, check.module_loadable, "Module Loadable"
    )
    set_module_result(
        check, check.check_name, loaded_check, check.module_loaded, "Module Loaded"
    )


def check_module_blacklisted(module_name):
    try:
        blacklist_result = subprocess.run(
            ["grep", "-r", f"blacklist {module_name}", "/etc/modprobe.d/"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        blacklist_output = blacklist_result.stdout.lower()
        return "blacklist" in blacklist_output
    except subprocess.CalledProcessError as e:
        print(f"Error checking if module {module_name} is denied: {e.stderr}")
        return False


def check_module_denied(module_name):
    try:
        install_result = subprocess.run(
            ["grep", "-r", f"install {module_name} /bin/false", "/etc/modprobe.d/"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        install_output = install_result.stdout.lower()
        return module_name.lower() in install_output
    except subprocess.CalledProcessError as e:
        print(f"Error checking if module {module_name} is denied: {e.stderr}")
        return False


def check_module_loadable(module_name):
    try:
        result = subprocess.run(
            ["sudo", "modprobe", module_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error checking if module {module_name} is loadable: {e.stderr}")
        return False


def check_module_loaded(module_name):
    try:
        result = subprocess.run(
            ["lsmod"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return module_name in result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error checking if module {module_name} is loaded: {e.stderr}")
        return False


def check_path(check):
    """
    Checks the existance and permissions of a file or directory.

    Args:
        check (Check): The check object.
    """
    path_exists = os.path.exists(check.check_path)
    expected_exists = check.path_exists

    # Path existence check
    if path_exists == expected_exists:
        result = "PASS"
    else:
        result = "FAIL"

    check.set_result({"name": check.check_name, "check": "Path Exists", "result": result})

    # Permissions check if path exists and is expected to exist
    if path_exists and expected_exists:
        perms_result = check_permissions(check)
        perms_result_text = "PASS" if perms_result else "FAIL"

        check.set_result(
            {
                "name": check.check_name,
                "check": "Path Permissions",
                "result": perms_result_text,
            }
        )


def check_permissions(check):
    """
    Checks the permissions of a file or directory.

    Args:
        check (Check): The check object.

    Returns:
        bool: True if the permissions match, False otherwise.
    """
    if os.path.exists(check.check_path):
        file_stats = os.stat(check.check_path)
        current_permissions = (
            file_stats.st_uid,
            file_stats.st_gid,
            int(oct(file_stats.st_mode)[-3:]),
        )
        expected_permissions = (
            check.expected_uid,
            check.expected_gid,
            check.expected_permissions,
        )
        return current_permissions == expected_permissions
    return False


def check_service(check):
    enabled_cmd = ["systemctl", "is-enabled", check.service_name]
    active_cmd = ["systemctl", "is-active", check.service_name]

    # Check the service status
    enabled_result = execute_systemctl(enabled_cmd)

    def set_service_result(check_name, check_type, expected, actual):
        result = "PASS" if expected == actual else "FAIL"
        check.set_result({"name": check_name, "check": check_type, "result": result})

    # Check service enabled status
    if enabled_result in ["enabled", "disabled", "masked"]:
        set_service_result(
            check.check_name,
            f"Service {enabled_result.capitalize()}",
            check.service_enabled,
            enabled_result == "enabled",
        )

        if enabled_result == "enabled":
            active_result = execute_systemctl(active_cmd)
            set_service_result(
                check.check_name,
                "Service Active",
                check.service_active,
                active_result == "active",
            )
    else:
        set_service_result(
            check.check_name, "Service Not Found", check.service_enabled, False
        )


def execute_systemctl(
    command,
):
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        if result.returncode == 0:
            return result.stdout.strip()
        elif result.returncode != 0 and len(result.stderr) > 0:
            return False
        else:
            return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        return e.stderr.strip()


# TODO
# def check_mount(check):
#     print("check_mount")
#     # Check if the mount exists

#     # Check if the mount is mounted

#     # Check the mount options


# TODO
# def check_mount_options(check):
#     print("check_mount_options")
#     command = ["findmnt", "-no", "OPTIONS", check.check_path]
#     result = execute_command(command)

#     status = False

#     # print(f"Mount options for {check.check_path}: {result}")

#     # print(type(result))

#     if result:
#         print(f"Mount options for {check.check_path}: {result}")
#         return True
#     else:
#         return False


# TODO
# def check_mount_point(check):
#     print("check_mount_point")


# TODO
# def check_package(check):
#     print("check_package")


# TODO
# def check_parameter(check):
#     print("check_parameter")
