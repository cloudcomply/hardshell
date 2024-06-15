import os
import subprocess
from src.hardshell.common.common import find_string


# TODO Check logic
def check_module(check):
    blacklisted_check = check_module_blacklisted(check.check_name)
    denied_check = check_module_denied(check.check_name)
    loadable_check = check_module_loadable(check.check_name)
    loaded_check = check_module_loaded(check.check_name)

    set_result(
        check=check,
        name=check.check_name,
        check_type=check.check_type.capitalize() + " Blacklisted",
        actual=blacklisted_check,
        expected=check.module_blacklisted,
    )
    set_result(
        check=check,
        name=check.check_name,
        check_type=check.check_type.capitalize() + " Denied",
        actual=denied_check,
        expected=check.module_denied,
    )
    set_result(
        check=check,
        name=check.check_name,
        check_type=check.check_type.capitalize() + " Loadable",
        actual=loadable_check,
        expected=check.module_loadable,
    )
    set_result(
        check=check,
        name=check.check_name,
        check_type=check.check_type.capitalize() + " Loaded",
        actual=loaded_check,
        expected=check.module_loaded,
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


def check_mount(check):
    # Check if mount exists
    mount_exists = check_mount_point(check.path)
    set_result(
        check=check,
        name=check.check_name,
        check_type=check.check_type.capitalize() + " Exists",
        actual=mount_exists,
        expected=True,
    )

    if mount_exists:
        # Check if separate partition
        seppart_result = check_mount_point_separate_partition(check.path)
        set_result(
            check=check,
            name=check.check_name,
            check_type=check.check_type.capitalize() + " Separate Partition",
            actual=seppart_result,
            expected=check.separate_partition,
        )

        # Check if mounted
        mounted_result = check_mount_point_status(check.path)

        if mounted_result:
            options_result = get_mount_point_options(check.path)

            # Check nodev option
            set_result(
                check=check,
                name=check.check_name,
                check_type=check.check_type.capitalize() + " Option: nodev",
                actual="nodev" in options_result,
                expected=check.nodev,
            )

            # Check noexec option
            set_result(
                check=check,
                name=check.check_name,
                check_type=check.check_type.capitalize() + " Option: noexec",
                actual="noexec" in options_result,
                expected=check.noexec,
            )

            # Check nosuid option
            set_result(
                check=check,
                name=check.check_name,
                check_type=check.check_type.capitalize() + " Option: nosuid",
                actual="nosuid" in options_result,
                expected=check.nosuid,
            )


def check_mount_point(path):
    """Check if the path is a mount point, including bind mounts."""
    try:
        result = subprocess.run(
            ["findmnt", "--target", path, "--output", "TARGET", "--noheadings"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return path in result.stdout.strip().splitlines()
    except subprocess.CalledProcessError:
        return False


def check_mount_point_bind_mount(path):
    """Check if the mount point is a bind mount."""
    try:
        result = subprocess.run(
            [
                "findmnt",
                "--target",
                path,
                "--output",
                "PROPAGATION,OPTIONS",
                "--noheadings",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return "bind" in result.stdout
    except subprocess.CalledProcessError:
        return False


def check_mount_point_separate_partition(path):
    """Check if the mount point is a separate partition from the root."""
    mount_device = get_mount_point_device(path)
    root_device = get_mount_point_device("/")
    return mount_device is not None and mount_device == root_device


def check_mount_point_status(path):
    """Check if the path is mounted."""
    try:
        result = subprocess.run(
            ["findmnt", "--target", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


# TODO Check Logic
def check_package(check, current_os, global_config):
    """Check if a package is installed based on the OS."""
    os_name = current_os.get("name", "").lower()

    os_mapping = {
        "ubuntu": "pkgmgr.ubuntu.command",
        "amzn": "pkgmgr.amzn.command",
        # "debian": "pkgmgr.debian.command",
        # "fedora": "pkgmgr.fedora.command",
        # "red hat": "pkgmgr.red_hat.command",
        # "rocky linux": "pkgmgr.rocky_linux.command",
        # "kali": "pkgmgr.kali.command",
    }

    attribute_path = os_mapping.get(os_name)

    if attribute_path:
        # Split the attribute path and dynamically access the nested attributes
        attrs = attribute_path.split(".")
        value = global_config
        for attr in attrs:
            value = getattr(value, attr, None)
            if value is None:
                break

        cmd = value.split()
        cmd.append(check.package_name)

        cmd_result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        if cmd_result.returncode == 0:
            # Use grep to filter the output for the at package
            grep_result = subprocess.run(
                ["grep", "-w", check.package_name],
                input=cmd_result.stdout,
                capture_output=True,
                text=True,
            )

            if grep_result.stdout.strip():
                set_result(
                    check=check,
                    name=check.check_name,
                    check_type=check.check_type.capitalize() + " Installed",
                    actual=True,
                    expected=check.package_install,
                )
            else:
                set_result(
                    check=check,
                    name=check.check_name,
                    check_type=check.check_type.capitalize() + " Installed",
                    actual=False,
                    expected=check.package_install,
                )
        else:
            pass

    else:
        print(f"No configuration found for OS: {os_name}")


def check_parameter(check, global_config):
    found_files = find_string(
        global_config.sysctl.directories, check.parameter, starts_with="#"
    )

    if len(found_files) > 0:
        set_result(
            check=check,
            name=check.check_name,
            check_type=check.check_type.capitalize() + " Found",
            actual=len(found_files) > 0,
            expected=True,
        )
    else:
        set_result(
            check=check,
            name=check.check_name,
            check_type=check.check_type.capitalize() + " Found",
            actual=len(found_files) > 0,
            expected=True,
        )


def check_path(check):
    """
    Checks the existance and permissions of a file or directory.

    Args:
        check (Check): The check object.
    """
    path_exists = os.path.exists(check.path)
    expected_exists = check.path_exists

    set_result(
        check=check,
        name=check.check_name,
        check_type=check.check_type.capitalize() + " Exists",
        actual=path_exists,
        expected=expected_exists,
    )

    # Permissions check if path exists and is expected to exist
    if path_exists and expected_exists:
        file_stats = os.stat(check.path)
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

        set_result(
            check=check,
            name=check.check_name,
            check_type=check.check_type.capitalize() + " Permissions",
            actual=current_permissions,
            expected=expected_permissions,
        )


def check_service(check):
    enabled_cmd = ["systemctl", "is-enabled", check.service_name]
    active_cmd = ["systemctl", "is-active", check.service_name]

    # Check the service status
    enabled_result = execute_systemctl(enabled_cmd)

    # Check service enabled status
    if enabled_result in ["enabled", "disabled", "masked"]:
        set_result(
            check=check,
            name=check.check_name,
            check_type=check.check_type.capitalize() + f" {enabled_result.capitalize()}",
            actual=enabled_result == "enabled",
            expected=check.service_enabled,
        )

        if enabled_result == "enabled":
            active_result = execute_systemctl(active_cmd)
            set_result(
                check=check,
                name=check.check_name,
                check_type=check.check_type.capitalize() + " Active",
                actual=active_result == "active",
                expected=check.service_active,
            )
    else:
        set_result(
            check=check,
            name=check.check_name,
            check_type=check.check_type.capitalize() + " Not Found",
            actual=False,
            expected=check.service_enabled,
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


def get_mount_point_device(path):
    """Get the device associated with the mount point."""
    try:
        result = subprocess.run(
            ["findmnt", "--target", path, "--output", "SOURCE", "--noheadings"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_mount_point_options(path):
    """Get the mount options for the mount point."""
    try:
        result = subprocess.run(
            [
                "findmnt",
                "--target",
                path,
                "--output",
                "OPTIONS",
                "--noheadings",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip().split(",")
    except subprocess.CalledProcessError:
        return []


def set_result(check, name, check_type, actual, expected):
    result = "PASS" if expected == actual else "FAIL"
    check.set_result({"name": name, "check": check_type, "result": result})
