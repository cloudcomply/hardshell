#########################################################################################
# Imports
#########################################################################################
import os
import subprocess
from hardshell.utils.common import path_exists, update_counts


def audit_linux(detected_os, global_config, linux_config):
    # Category names and their corresponding checks
    categories = {
        "Accounts": linux_config.get("accounts"),
        "Aide": linux_config.get("aide"),
        "Audit": linux_config.get("audit"),
        "Banners": linux_config.get("banners"),
        "Filesystem-Mounts": linux_config.get("filesystem", {}).get("mounts"),
        "Logging-Rsyslog": linux_config.get("logging", {}).get("rsyslog"),
        "Kernel-Modules": linux_config.get("kernel", {}).get("modules"),
        "Kernel-Parameters": linux_config.get("kernel", {}).get("parameters"),
        "Restricted-Packages": linux_config.get("restricted", {}).get("packages"),
        "Restricted-Services": linux_config.get("restricted", {}).get("services"),
        "Schedulers-At": linux_config.get("schedulers", {}).get("at"),
        "Schedulers-Cron": linux_config.get("schedulers", {}).get("cron"),
        "SELinux": linux_config.get("selinux"),
        "Sudo": linux_config.get("sudo"),
        "Time-Chrony": linux_config.get("time", {}).get("chrony"),
        "Time-Timesyncd": linux_config.get("time", {}).get("systemd-timesyncd"),
    }

    # Current OS version string
    current_os = f"{detected_os['id']}-{detected_os['version_id']}"

    # Loop through the categories and perform checks
    for category, checks in categories.items():
        if checks:
            audit_checks(
                global_config=global_config,
                category=category,
                current_os=current_os,
                checks=checks,
            )


def audit_checks(global_config, category, current_os, checks):
    check_handlers = {
        # "file-exists": ("file", check_file_exists),  # Good
        # "kernel-module": ("module", check_module),
        # "kernel-parameter": ("parameter", check_parameter),
        # "mount-options": ("mount", check_mount),  # Good
        "package": ("package", check_package),  # Not Good...
        # "permissions": ("permissions", check_permissions),  # Good
        # "service": ("service", check_service),  # Good
    }

    failed_checks = 0
    passed_checks = 0

    for check, check_data in checks.items():
        if current_os in check_data["valid_os"]:
            check_type = check_data["check_type"]
            arg_key, handler = check_handlers.get(check_type, (None, None))

            if handler:
                # Build arguments dictionary dynamically
                args = {arg_key: check_data} if arg_key else {}

                # Add global_config to args if needed by the handler
                if check_type in ["mount-options", "package"]:
                    args["global_config"] = global_config

                if check_type in ["package"]:
                    args["current_os"] = current_os

                output = handler(**args)

                if output:
                    passed_checks += 1
                else:
                    failed_checks += 1

    update_counts(
        category=category, passed_checks=passed_checks, failed_checks=failed_checks
    )


def execute_command(command, expect_output=True):
    # print(f"executing commmand: {command}")
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        print(f"result: {result}")

        output = result.stdout.strip()

        print(f"output: {output}")

        if expect_output:
            return output
        return output != ""
    except subprocess.CalledProcessError:
        return False


def execute_grep_command(command, module):
    module_process = subprocess.Popen(
        command, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, text=True
    )

    grep_process = subprocess.Popen(
        ["grep", module],
        stdin=module_process.stdout,
        stdout=subprocess.PIPE,
        text=True,
    )

    module_process.stdout.close()
    output = grep_process.communicate()[0]

    return output


def check_file_exists(file):
    if file["file_exists"] == True and path_exists(file["check_path"]) == True:
        return True
    return False


def check_mount(global_config, mount):
    # Execute the command to get the mount options
    command = ["findmnt", "-no", "OPTIONS", mount["check_path"]]
    mount_options_str = execute_command(command)

    # Check if the mount point exists by evaluating the output of the command
    if mount_options_str:
        print(f"Mount point found for {mount['check_name']} at {mount['check_path']}")
        mount_options = set(mount_options_str.split(","))
        all_options_present = True

        for option in mount["mount_options"]:
            if option in mount_options:
                print(f"Option: {option} is set at Mount Point: {mount['check_path']}")
            else:
                print(
                    f"Option: {option} is NOT set at Mount Point: {mount['check_path']}"
                )
                all_options_present = False  # Once set to False, it remains False

        return all_options_present
    else:
        print(
            f"No mount point found for {mount['check_path']}. Assuming default check status as True."
        )
        return True  # Return True if the mount point does not exist


# TODO Fix this
def check_package(current_os, global_config, package):
    package_name = package["package_name"]
    distro = current_os.split("-")[0]

    command_template = (
        global_config.get("global", {}).get(distro, {}).get("package_search", [])
    )
    command = command_template + [package_name]

    result = execute_command(command)

    print(f"Package Result: {result}")

    if not result:
        print(f"Package {package_name} is not installed.")
        if package.get("package_status") == "install":
            print(f"{package_name} should be installed.")
            return False
        return package.get("package_status") == "remove"

    # Result is valid, checking installation status
    is_installed = "installed" in result
    expected_status = package.get("package_status")

    if is_installed:
        if expected_status == "install":
            print(f"Package {package_name} is correctly installed.")
            return True
        elif expected_status == "remove":
            print(f"Package {package_name} is installed but should be removed.")
            return False
    else:
        print(f"Package {package_name} is not installed.")
        if expected_status == "install":
            print(f"{package_name} should be installed.")
            return True
        return False


def check_permissions(permissions):
    if os.path.exists(permissions["check_path"]):
        file_stats = os.stat(permissions["check_path"])
        current_permissions = (
            file_stats.st_uid,
            file_stats.st_gid,
            int(oct(file_stats.st_mode)[-3:]),
        )
        expected_permissions = (
            permissions.get("expected_uid"),
            permissions.get("expected_gid"),
            permissions.get("expected_permissions"),
        )
        return current_permissions == expected_permissions
    return False


def check_service(service):
    service_name = service["service_name"]
    service_required_status = service["service_status"]

    # Check if the service is enabled
    is_enabled = execute_command(["systemctl", "is-enabled", service_name])
    is_active = execute_command(["systemctl", "is-active", service_name])

    # Print service status information
    print(
        f"Service {service_name} is {'enabled' if is_enabled else 'disabled'}, {'active' if is_active else 'inactive'}."
    )

    # Return True if the service is both enabled and active as required
    if service_required_status == "enabled":
        # print(is_enabled)
        # print(is_active)
        return is_enabled and is_active
    else:
        # For different logic on service_required_status other than 'enabled', handle accordingly
        print(not is_enabled and not is_active)
        return not is_enabled and not is_active


# TODO fix this
def check_module(module):
    print(f"Checking module: {module['module_name']}")

    module_name = module["module_name"]

    # command = ["modprobe", "-n", "-v", module["module_name"]]
    # modprobe = execute_command(command, expect_output=True)

    command = ["modprobe", "--showconfig"]
    modprobe = execute_grep_command(command, module["module_name"])

    if modprobe:
        # print(modprobe)
        if (
            f"install {module_name} /bin/false" in modprobe
            or f"install {module_name} /bin/true" in modprobe
            and f"blacklist {module['module_name']}" in modprobe
            and module["module_status"] == "deny"
        ):
            print(f"Module: {module['module_name']} is denied.")
            return True

        elif (
            f"install {module_name} /bin/false" in modprobe
            or f"install {module_name} /bin/true" in modprobe
            and f"blacklist {module['module_name']}" in modprobe
            and module["module_status"] == "allow"
        ):
            print(f"Module: {module['module_name']} is denied, but allowed.")
            return False

        elif (
            f"install {module_name} /bin/false" not in modprobe
            or f"install {module_name} /bin/true" not in modprobe
            and f"blacklist {module['module_name']}" not in modprobe
            and module["module_status"] == "deny"
        ):
            print(f"Module: {module['module_name']} is not denied.")
            return False
        elif (
            f"install {module_name} /bin/false" not in modprobe
            or f"install {module_name} /bin/true" not in modprobe
            and f"blacklist {module['module_name']}" not in modprobe
            and module["module_status"] == "allow"
        ):
            print(f"Module: {module['module_name']} is not denied.")

            command = ["lsmod", "|", "grep", module["module_name"]]
            loaded = execute_command(command, expect_output=True)

            print(loaded)

            if loaded:
                print(f"Module: {module['module_name']} is loaded.")
                return True

            # return False
    else:
        print(f"Module: {module['module_name']} is not denied.")
        return False

    # return False

    # command = ["lsmod", "|", "grep", module["module_name"]]
    # loaded = execute_command(command, expect_output=True)

    # if loaded and module["module_status"] == "allow":
    #     print(f"Module: {module['module_name']} is loaded and allowed.")
    #     return True
    # elif loaded and module["module_status"] == "deny":
    #     print(f"Module: {module['module_name']} is loaded and denied.")
    #     return False
    # else:
    #     print(f"Module: {module['module_name']} is not loaded and denied.")
    #     return True


# Old code
