import glob
import os
import subprocess
from datetime import datetime
from src.hardshell.common.common import (
    find_pattern_in_directory,
    find_pattern_in_file,
    get_config_mapping,
    get_pkgmgr_mapping,
)


def check_accounts(check):
    user_names, user_uids, group_names, group_gids = set(), set(), set(), set()
    cleartext_pw_users = []
    duplicates = {
        "group_names": [],
        "user_names": [],
        "user_uids": [],
        "group_gids": [],
    }
    root_uid_count = 0
    existing_group_names = set()
    shadowed_passwords = set()
    missing_shadowed_passwords = []
    users_with_future_changes = []
    missing_groups = []
    uid_min = 1000  # Default value, to be read from /etc/login.defs

    def process_passwd_line(line):
        nonlocal root_uid_count
        user_name, user_pass, user_uid, user_gid = line.strip().split(":")[:4]

        if user_name == "root":
            set_result(check, "root uid", "root uid", user_uid == "0")
            set_result(check, "root gid", "root gid", user_gid == "0")

        if user_uid == "0":
            root_uid_count += 1

        if user_pass not in {"x", "*"}:
            cleartext_pw_users.append(user_name)

        check_duplicates(user_name, user_names, duplicates["user_names"])
        check_duplicates(user_uid, user_uids, duplicates["user_uids"])

        if user_gid not in existing_group_names:
            group_gids.add(user_gid)

        shadowed_passwords.add(user_name)

    def process_group_line(line):
        group_name, group_gid = (
            line.strip().split(":")[0],
            line.strip().split(":")[2],
        )
        existing_group_names.add(group_gid)
        check_duplicates(group_name, group_names, duplicates["group_names"])
        check_duplicates(group_gid, group_gids, duplicates["group_gids"])

    def process_shadow_line(line):
        user_name, shadowed_pass = line.strip().split(":")[:2]

        if user_name in shadowed_passwords and (
            not shadowed_pass or shadowed_pass == ""
        ):
            missing_shadowed_passwords.append(user_name)

        if (
            shadowed_pass not in ("!", "*")
            and user_name not in missing_shadowed_passwords
        ):
            last_change_date = get_last_password_change(user_name)
            if last_change_date and last_change_date > datetime.now():
                users_with_future_changes.append(user_name)

    def check_duplicates(item, item_set, duplicate_list):
        if item in item_set:
            duplicate_list.append(item)
        else:
            item_set.add(item)

    def get_last_password_change(user):
        try:
            with open("/etc/shadow", "r") as f:
                for line in f:
                    fields = line.strip().split(":")
                    if fields[0] == user:
                        last_change = int(fields[2])
                        return datetime.fromtimestamp(
                            last_change * 24 * 60 * 60
                        )
        except Exception as e:
            print(
                f"Error retrieving last password change date for {user}: {e}"
            )
        return None

    def read_uid_min():
        nonlocal uid_min
        try:
            with open("/etc/login.defs", "r") as f:
                for line in f:
                    if line.startswith("UID_MIN"):
                        uid_min = int(line.split()[1])
                        break
        except Exception as e:
            print(f"Error reading UID_MIN from /etc/login.defs: {e}")

    def check_system_accounts():
        critical_accounts = []
        try:
            with open("/etc/passwd", "r") as f:
                for line in f:
                    fields = line.strip().split(":")
                    user_name, user_uid, shell = (
                        fields[0],
                        int(fields[2]),
                        fields[6],
                    )
                    if (
                        user_name
                        not in {
                            "root",
                            "halt",
                            "sync",
                            "shutdown",
                            "nfsnobody",
                        }
                        and (user_uid < uid_min or user_uid == 65534)
                        and not shell.endswith("nologin")
                    ):
                        critical_accounts.append(user_name)
        except Exception as e:
            print(f"Error checking system accounts: {e}")
        return critical_accounts

    def check_disabled_accounts():
        disabled_accounts = []
        try:
            with open("/etc/passwd", "r") as f:
                nologin_users = [
                    line.split(":")[0]
                    for line in f
                    if line.strip().split(":")[6].endswith("nologin")
                ]
            for user in nologin_users:
                with open("/etc/shadow", "r") as f:
                    for line in f:
                        fields = line.strip().split(":")
                        if fields[0] == user and not fields[1].startswith(
                            ("!", "*")
                        ):
                            disabled_accounts.append(user)
        except Exception as e:
            print(f"Error checking disabled accounts: {e}")
        return disabled_accounts

    def check_root_password():
        try:
            with open("/etc/shadow", "r") as f:
                for line in f:
                    fields = line.strip().split(":")
                    if fields[0] == "root":
                        shadowed_pass = fields[1]
                        if shadowed_pass in ("!", "*", "*LOCK*"):
                            return True
                        elif len(shadowed_pass) > 0:
                            return True
                        return False
        except Exception as e:
            print(f"Error checking root password: {e}")
            return False

    read_uid_min()

    with open("/etc/group", "r") as f:
        for line in f:
            process_group_line(line)

    with open("/etc/passwd", "r") as f:
        for line in f:
            user_gid = line.strip().split(":")[3]
            if user_gid not in group_gids:
                missing_groups.append(user_gid)
            process_passwd_line(line)

    with open("/etc/shadow", "r") as f:
        for line in f:
            process_shadow_line(line)

    system_accounts = check_system_accounts()
    disabled_accounts = check_disabled_accounts()
    root_password_set = check_root_password()

    set_result(
        check,
        "user uses shadowed password",
        "password",
        not cleartext_pw_users,
    )
    set_result(
        check,
        "all users have shadowed passwords",
        "password",
        not missing_shadowed_passwords,
    )
    set_result(check, "user names", "duplicate", not duplicates["user_names"])
    set_result(check, "user uids", "duplicate", not duplicates["user_uids"])
    set_result(
        check, "group names", "duplicate", not duplicates["group_names"]
    )
    set_result(check, "group gids", "duplicate", not duplicates["group_gids"])
    set_result(
        check, "root uid unique", "root uid unique", root_uid_count == 1
    )
    set_result(
        check, "all group names exist", "group existence", not missing_groups
    )
    set_result(
        check,
        "all users' last password change date is in the past",
        "password change",
        not users_with_future_changes,
    )
    set_result(
        check,
        "critical system accounts secured",
        "system accounts",
        not system_accounts,
    )
    set_result(
        check,
        "nologin accounts passwords disabled",
        "disabled accounts",
        not disabled_accounts,
    )
    set_result(check, "root password set", "root password", root_password_set)


# TODO Check logic
def check_module(check):
    blacklisted_check = check_module_blacklisted(check.check_name)
    denied_check = check_module_denied(check.check_name)
    loadable_check = check_module_loadable(check.check_name)
    loaded_check = check_module_loaded(check.check_name)

    set_result(
        check=check,
        name=check.check_name,
        check_type=f"{check.check_type} blacklisted",
        actual=blacklisted_check,
        expected=check.module_blacklisted,
    )
    set_result(
        check=check,
        name=check.check_name,
        check_type=f"{check.check_type} denied",
        actual=denied_check,
        expected=check.module_denied,
    )
    set_result(
        check=check,
        name=check.check_name,
        check_type=f"{check.check_type} loadable",
        actual=loadable_check,
        expected=check.module_loadable,
    )
    set_result(
        check=check,
        name=check.check_name,
        check_type=f"{check.check_type} loaded",
        actual=loaded_check,
        expected=check.module_loaded,
    )


# TODO Convert to regex
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


# TODO Convert to regex
def check_module_denied(module_name):
    try:
        install_result = subprocess.run(
            [
                "grep",
                "-r",
                f"install {module_name} /bin/false",
                "/etc/modprobe.d/",
            ],
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
            # ["sudo", "modprobe", module_name],
            ["modprobe", module_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(
            f"Error checking if module {module_name} is loadable: {e.stderr}"
        )
        return False


def check_module_loaded(module_name):
    try:
        result = subprocess.run(
            ["lsmod"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
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
        check_type=f"{check.check_type} exists",
        actual=mount_exists,
        expected=True,
    )
    if mount_exists:
        # Check if mounted at boot
        boot_result = check_mount_point_boot(check.path)
        set_result(
            check=check,
            name=check.check_name,
            check_type=f"{check.check_type} boot",
            actual=boot_result,
            expected=check.mount_boot,
        )
        # Check if separate partition
        seppart_result = check_mount_point_separate_partition(check.path)
        set_result(
            check=check,
            name=check.check_name,
            check_type=f"{check.check_type} separate partition",
            actual=seppart_result,
            expected=check.separate_partition,
        )
        # Check if mounted
        mounted_result = check_mount_point_mounted(check.path)
        if mounted_result:
            options_result = get_mount_point_options(check.path)
            # Check nodev option
            set_result(
                check=check,
                name=check.check_name,
                check_type=f"{check.check_type} Option: nodev",
                actual="nodev" in options_result,
                expected=check.nodev,
            )
            # Check noexec option
            set_result(
                check=check,
                name=check.check_name,
                check_type=f"{check.check_type} Option: noexec",
                actual="noexec" in options_result,
                expected=check.noexec,
            )
            # Check nosuid option
            set_result(
                check=check,
                name=check.check_name,
                check_type=f"{check.check_type} Option: nosuid",
                actual="nosuid" in options_result,
                expected=check.nosuid,
            )


def check_mount_point(path):
    """Check if the path is a mount point, including bind mounts."""
    try:
        result = subprocess.run(
            [
                "findmnt",
                "--target",
                path,
                "--output",
                "TARGET",
                "--noheadings",
            ],
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


# TODO Check for mount point at boot
def check_mount_point_boot(path):
    return False


def check_mount_point_mounted(path):
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


def check_package(check, current_os, global_config):
    """Check if a package is installed based on the OS."""
    os_name = current_os.get("id", None).lower()
    if os_name is not None:
        pkgmgr = get_pkgmgr_mapping(global_config, os_name)
        cmd = pkgmgr.split()
        cmd.append(check.package_name)
        try:
            cmd_result = subprocess.run(cmd, capture_output=True, text=True)
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
                        check_type=f"{check.check_type}",
                        actual=True,
                        expected=check.package_install,
                    )
            else:
                set_result(
                    check=check,
                    name=check.check_name,
                    check_type=f"{check.check_type}",
                    actual=False,
                    expected=check.package_install,
                )

        except subprocess.CalledProcessError as e:
            print(
                f"Error checking if package {check.package_name} is installed: {e}"
            )
    else:
        print(f"No configuration found for OS: {os_name}")


def check_path(check):
    path_exists = os.path.exists(check.path)
    expected_exists = check.path_exists
    # Permissions check if path exists and is expected to exist
    if path_exists and expected_exists:
        if os.path.isfile(check.path):
            # print(f"Path is a file: {check.path}")
            file_stats = get_permissions(check.path)
            current_permissions = (
                file_stats.st_uid,
                file_stats.st_gid,
                int(oct(file_stats.st_mode)[-3:]),
            )
            set_result(
                check=check,
                name=check.check_name,
                check_type=f"{check.check_type}",
                actual=current_permissions,
                expected=tuple(check.expected_perms),
            )
        else:
            if check.check_files == True:
                all_paths = glob.glob(
                    os.path.join(check.path, "**", "*"), recursive=True
                )
                for path in all_paths:
                    file_stats = get_permissions(path)
                    current_permissions = (
                        file_stats.st_uid,
                        file_stats.st_gid,
                        int(oct(file_stats.st_mode)[-3:]),
                    )
                    set_result(
                        check=check,
                        name=f"{check.check_name} - {path}",
                        check_type=f"{check.check_type}",
                        actual=current_permissions,
                        expected=tuple(check.expected_perms),
                    )

            dir_stats = get_permissions(check.path)
            current_permissions = (
                dir_stats.st_uid,
                dir_stats.st_gid,
                int(oct(dir_stats.st_mode)[-3:]),
            )
            set_result(
                check=check,
                name=check.check_name,
                check_type=f"{check.check_type}",
                actual=current_permissions,
                expected=tuple(check.expected_perms),
            )
    else:
        set_result(
            check=check,
            name=check.check_name,
            check_type=f"{check.check_type}",
            actual=False,
            expected=expected_exists,
        )


# TODO Maybe logic problem?
def check_regex(check, global_config):
    pattern_found = False
    pattern_line = ""

    if check.category is not None:
        paths = get_config_mapping(check, global_config)
        for path in paths:
            if os.path.isfile(path):
                result = find_pattern_in_file(path, check.pattern)
                pattern_found = result[0]
                pattern_line = result[1]
            elif os.path.isdir(path):
                result = find_pattern_in_directory(
                    path, check.pattern, check.file_extension
                )
                pattern_found = result[0]
                pattern_line = result[1]
            if pattern_found:
                break

    if check.pattern_exists == False:
        set_result(
            check=check,
            name=check.check_name,
            check_type=f"{check.check_type}",
            actual=check.pattern_exists == False and pattern_found == False,
        )
    else:
        set_result(
            check=check,
            name=check.check_name,
            check_type=f"{check.check_type}",
            actual=pattern_found,
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
            check_type=f"{check.check_type} {enabled_result}",
            actual=enabled_result == "enabled",
            expected=check.service_enabled,
        )

        if enabled_result == "enabled":
            active_result = execute_systemctl(active_cmd)
            set_result(
                check=check,
                name=check.check_name,
                check_type=f"{check.check_type}",
                actual=active_result == "active",
                expected=check.service_active,
            )
    else:
        set_result(
            check=check,
            name=check.check_name,
            check_type=f"{check.check_type}",
            actual=False,
            expected=check.service_enabled,
        )


def check_ssh_keys(check):
    paths = glob.glob(os.path.join(check.path, "*"))
    files = [
        f
        for f in paths
        if os.path.isfile(f) and detect_openssh_key(f) == check.category
    ]

    for file in files:
        file_stats = os.stat(file)
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
            check_type=f"{check.check_type} Permissions",
            actual=current_permissions,
            expected=expected_permissions,
        )


def check_unconfined_services(check):
    unconfined_services = []

    # List all process IDs in the /proc directory
    for pid in os.listdir("/proc"):
        if pid.isdigit():
            try:
                # Read the SELinux security context for the process
                with open(f"/proc/{pid}/attr/current", "r") as f:
                    selinux_context = f.read().strip()

                # Check if the context contains 'unconfined_service_t'
                if "unconfined_service_t" in selinux_context:
                    with open(f"/proc/{pid}/comm", "r") as comm_file:
                        process_name = comm_file.read().strip()
                    unconfined_services.append((pid, process_name))
            except FileNotFoundError:
                continue
            except PermissionError:
                continue
            except Exception as e:
                pass

    set_result(
        check=check,
        name=check.check_name,
        check_type=f"{check.check_type}",
        actual=not unconfined_services,
    )


def detect_openssh_key(path):
    """
    Detect if a file is an OpenSSH private or public key.

    :param file_path: Path to the file to check.
    :return: A string indicating the type of key ('OpenSSH private key', 'OpenSSH public key') or 'Unknown'.
    """
    private_key_headers = [
        "-----BEGIN DSA PRIVATE KEY-----",
        "-----BEGIN EC PRIVATE KEY-----",
        "-----BEGIN OPENSSH PRIVATE KEY-----",
        "-----BEGIN RSA PRIVATE KEY-----",
    ]
    public_key_prefixes = [
        "ecdsa-sha2-nistp256",
        "ecdsa-sha2-nistp384",
        "ecdsa-sha2-nistp521",
        "ssh-dss",
        "ssh-ed25519",
        "ssh-rsa",
    ]

    try:
        with open(path, "r") as file:
            first_line = file.readline().strip()

            # Check for OpenSSH private key headers
            if first_line in private_key_headers:
                return "private"

            # Check for OpenSSH public key prefixes
            for prefix in public_key_prefixes:
                if first_line.startswith(prefix):
                    return "public"

        return "unknown"
    except Exception as e:
        return f"Error reading file: {e}"


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
            [
                "findmnt",
                "--target",
                path,
                "--output",
                "SOURCE",
                "--noheadings",
            ],
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


def get_permissions(path):
    return os.stat(path)


def set_result(check, name, check_type, actual, expected=None):
    if expected is not None:
        result = "pass" if expected == actual else "fail"
    elif check.check_type == "regex":
        result = "pass" if actual else "fail"
    else:
        result = "pass" if actual else "fail"
    check.set_result({"name": name, "check": check_type, "result": result})


# TODO Fix this
def check_command(check):
    print("Checking command")
    print(check.command)
    print(list(check.command.split()))

    cmd = list(check.command.split())

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        print(result)

    # if result.returncode == 0 and len(result.stdout) > 0:
    #     set_result(
    #         check=check,
    #         name=check.check_name,
    #         check_type=f"{check.check_type}",
    #         actual=True,
    #     )
    # else:
    #     set_result(
    #         check=check,
    #         name=check.check_name,
    #         check_type=f"{check.check_type}",
    #         actual=False,
    #     )

    except FileNotFoundError as e:
        # print(f"Error running command: {e}")
        pass


def test_command():
    pass
