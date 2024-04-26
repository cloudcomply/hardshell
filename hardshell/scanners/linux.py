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
        # "file-exists": ("file", check_file_exists),
        "kernel-module": ("module", check_module),
        # "kernel-parameter": ("parameter", check_parameter),
        # "mount-options": ("mount", check_mount),
        # "package": ("package", check_package),
        # "permissions": ("permissions", check_permissions),
        # "service": ("service", check_service),
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
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        output = result.stdout.strip()
        if expect_output:
            return output
        return output != ""
    except subprocess.CalledProcessError:
        return False


def check_module(module):
    # print(module)
    loaded = execute_command(
        ["lsmod", "|", "grep", module["module_name"]],
        expect_output=True,
    )
    print(f"Loaded: {loaded}")


# def check_module(current_os, module):
#     loaded = execute_command(["lsmod"], expect_output=True)
#     return module["module_name"] in loaded and not module.get("deny", False)


# Old code


# def audit_linux(detected_os, global_config, linux_config):
#     accounts = linux_config.get("accounts")
#     aide = linux_config.get("aide")
#     audit = linux_config.get("audit")
#     banners = linux_config.get("banners")
#     filesystem_mounts = linux_config.get("filesystem").get("mounts")
#     logging_rsyslog = linux_config.get("logging").get("rsyslog")
#     modules = linux_config.get("kernel").get("modules")
#     parameters = linux_config.get("kernel").get("parameters")
#     restricted_packages = linux_config.get("restricted").get("packages")
#     restricted_services = linux_config.get("restricted").get("services")
#     schedulers_at = linux_config.get("schedulers").get("at")
#     schedulers_cron = linux_config.get("schedulers").get("cron")
#     selinux = linux_config.get("selinux")
#     sudo = linux_config.get("sudo")
#     time_chrony = linux_config.get("time").get("chrony")
#     time_timesyncd = linux_config.get("time").get("systemd-timesyncd")

#     current_os = f"{detected_os['id']}-{detected_os['version_id']}"

#     if accounts:
#         audit_checks(
#             global_config=global_config,
#             category="Accounts",
#             current_os=current_os,
#             checks=accounts,
#         )

#     if aide:
#         audit_checks(
#             global_config=global_config,
#             category="Aide",
#             current_os=current_os,
#             checks=aide,
#         )

#     if audit:
#         audit_checks(
#             global_config=global_config,
#             category="Audit",
#             current_os=current_os,
#             checks=audit,
#         )

#     if banners:
#         audit_checks(
#             global_config=global_config,
#             category="Banners",
#             current_os=current_os,
#             checks=banners,
#         )

#     if filesystem_mounts:
#         audit_checks(
#             global_config=global_config,
#             category="Filesystem-Mounts",
#             current_os=current_os,
#             checks=filesystem_mounts,
#         )

#     if logging_rsyslog:
#         audit_checks(
#             global_config=global_config,
#             category="Logging-Rsyslog",
#             current_os=current_os,
#             checks=logging_rsyslog,
#         )

#     if modules:
#         audit_checks(
#             global_config=global_config,
#             category="Kernel-Modules",
#             current_os=current_os,
#             checks=modules,
#         )

#     if parameters:
#         audit_checks(
#             global_config=global_config,
#             category="Kernel-Parameters",
#             current_os=current_os,
#             checks=parameters,
#         )

#     if restricted_packages:
#         audit_checks(
#             global_config=global_config,
#             category="Restricted-Packages",
#             current_os=current_os,
#             checks=restricted_packages,
#         )

#     if restricted_services:
#         audit_checks(
#             global_config=global_config,
#             category="Restricted-Services",
#             current_os=current_os,
#             checks=restricted_services,
#         )

#     if schedulers_at:
#         audit_checks(
#             global_config=global_config,
#             category="Schedulers-At",
#             current_os=current_os,
#             checks=schedulers_at,
#         )

#     if schedulers_cron:
#         audit_checks(
#             global_config=global_config,
#             category="Schedulers-Cron",
#             current_os=current_os,
#             checks=schedulers_cron,
#         )

#     if selinux:
#         audit_checks(
#             global_config=global_config,
#             category="SELinux",
#             current_os=current_os,
#             checks=selinux,
#         )

#     if sudo:
#         audit_checks(
#             global_config=global_config,
#             category="Sudo",
#             current_os=current_os,
#             checks=sudo,
#         )

#     if time_chrony:
#         audit_checks(
#             global_config=global_config,
#             category="Time-Chrony",
#             current_os=current_os,
#             checks=time_chrony,
#         )

#     if time_timesyncd:
#         audit_checks(
#             global_config=global_config,
#             category="Time-Timesyncd",
#             current_os=current_os,
#             checks=time_timesyncd,
#         )


# def audit_checks(
#     global_config,
#     category,
#     current_os,
#     checks,
# ):
#     failed_checks = 0
#     passed_checks = 0

#     for check in checks:
#         if current_os in checks[check]["valid_os"]:
#             if checks[check]["check_type"] == "file-exists":
#                 output = check_file_exists(
#                     current_os=current_os,
#                     file=checks[check],
#                 )
#                 if output:
#                     passed_checks += 1
#                 else:
#                     failed_checks += 1
#             elif checks[check]["check_type"] == "kernel-module":
#                 output = check_module(
#                     current_os=current_os,
#                     module=checks[check],
#                 )
#                 if output:
#                     passed_checks += 1
#                 else:
#                     failed_checks += 1
#             elif checks[check]["check_type"] == "kernel-parameter":
#                 output = check_parameter(
#                     current_os=current_os,
#                     parameter=checks[check],
#                 )
#                 if output:
#                     passed_checks += 1
#                 else:
#                     failed_checks += 1
#             elif checks[check]["check_type"] == "mount-options":
#                 output = check_mount(
#                     current_os=current_os,
#                     global_config=global_config,
#                     mount=checks[check],
#                 )

#                 if output:
#                     passed_checks += 1
#                 else:
#                     failed_checks += 1
#             elif checks[check]["check_type"] == "package":
#                 output = check_package(
#                     current_os=current_os,
#                     global_config=global_config,
#                     package=checks[check],
#                 )
#                 if output:
#                     passed_checks += 1
#                 else:
#                     failed_checks += 1
#             elif checks[check]["check_type"] == "permissions":
#                 output = check_permissions(
#                     current_os=current_os,
#                     permissions=checks[check],
#                 )
#                 if output:
#                     passed_checks += 1
#                 else:
#                     failed_checks += 1
#             elif checks[check]["check_type"] == "service":
#                 output = check_service(
#                     current_os=current_os,
#                     service=checks[check],
#                 )
#                 if output:
#                     passed_checks += 1
#                 else:
#                     failed_checks += 1

#     update_counts(
#         category=category,
#         passed_checks=passed_checks,
#         failed_checks=failed_checks,
#     )


# def path_exists(path):
#     if os.path.exists(path):
#         return True
#     else:
#         return False


# def check_file_exists(current_os, file):
#     check_status = False

#     output = verify_command(
#         [
#             "file",
#             file["check_path"],
#         ]
#     )

#     if len(output.stdout) > 0 and file["check_path"] == True:
#         check_status = True
#     else:
#         check_status = False

#     return check_status


# def check_module(current_os, module):
#     """
#     Scan kernel modules for loaded, loadable, and deny listed
#     :param current_os: The current operating system
#     :param modules: The list of kernel modules to scan
#     """
#     check_status = False
#     module_name = module["module_name"]

#     # Check for Loadable
#     loadable = False

#     if loadable:
#         check_status = False
#     else:
#         check_status = True

#     # Check for Loaded
#     loaded = verify_lsmod(module_name)

#     if loaded:
#         check_status = False
#     else:
#         check_status = True

#     # Check for deny listed
#     denied = False

#     if denied:
#         check_status = False
#     else:
#         check_status = True

#     return check_status


# def check_mount(current_os, global_config, mount):
#     check_status = False

#     output = verify_command(
#         [
#             "findmnt",
#             mount["check_path"],
#         ]
#     )

#     for option in mount["mount_options"]:
#         if len(output.stdout) > 0:
#             if option in output.stdout:
#                 # print(f"{option} not on {mount['check_path']}")
#                 check_status = True
#             else:
#                 # print(f"{option} on {mount['check_path']}")
#                 check_status = False
#         else:
#             check_status = True

#     return check_status


# def check_package(current_os, global_config, package):
#     check_status = False

#     # print(package)

#     distro = current_os.split("-")[0]
#     # cmd_install = global_config.get("global").get(distro).get("package_install")
#     # cmd_remove = global_config.get("global").get(distro).get("package_remove")
#     cmd_search = global_config.get("global").get(distro).get("package_search")
#     package_name = package["package_name"]

#     # Check Package Status
#     status = verify_package(pkgmgr=cmd_search, package=package_name)

#     if status and package["package_status"] == "install":
#         check_status = True
#     elif status and package["package_status"] == "remove":
#         check_status = False
#     elif status and package["package_status"] == "required":
#         check_status = True
#     elif not status and package["package_status"] == "install":
#         check_status = False
#     elif not status and package["package_status"] == "remove":
#         check_status = True
#     elif not status and package["package_status"] == "required":
#         check_status = False

#     return check_status


# def check_parameter(current_os, parameter):
#     # print(parameter)
#     check_status = False
#     return check_status


# def check_permissions(current_os, permissions):
#     # print(permissions)
#     check_status = False

#     if path_exists(permissions["check_path"]):
#         uid, gid, perms = get_permissions(permissions["check_path"])
#         if (
#             uid == permissions.get("expected_uid")
#             and gid == permissions.get("expected_gid")
#             and int(perms) == permissions.get("expected_permissions")
#         ):
#             # print("PASS")
#             check_status = True
#         else:
#             # print("FAIL")
#             # # print(f"uid: {uid}")
#             # # print(f"gid: {gid}")
#             # # print(f"permissions: {permissions}")
#             check_status = False

#     return check_status


# def check_service(current_os, service):
#     check_status = False
#     service_name = service["service_name"]

#     cmd_active = ["systemctl", "is-active", f"{service_name}"]
#     cmd_enabled = ["systemctl", "is-enabled", f"{service_name}"]

#     check_enabled = verify_service(cmd_enabled)

#     if (
#         len(check_enabled.stdout) > 0
#         and "enabled" in check_enabled.stdout
#         and "enabled" == service["service_status"]
#     ):
#         # print(strip_non_alphabetical(check_enabled.stdout))
#         print(f"Service {service_name} is enabled.")
#         check_status = True

#         if check_status:
#             check_active = verify_service(cmd_active)

#             if len(check_active.stdout) > 0 and "active" in check_active.stdout:
#                 print(f"Service {service_name} is active.")
#                 check_status = True
#             else:
#                 print(f"Service {service_name} is not active.")
#                 check_status = False
#     elif (
#         len(check_enabled.stdout) > 0
#         and "masked" in check_enabled.stdout
#         and "masked" == service["service_status"]
#     ):
#         # print(f"Service {service_name} is masked.")
#         check_status = True
#     else:
#         # print(f"Service {service_name} is disabled.")
#         check_status = False

#     return check_status


# def get_permissions(path):
#     try:
#         st = os.stat(path)
#         permissions = oct(st.st_mode & 0o777)
#         return st.st_uid, st.st_gid, permissions[-3:]
#     except FileNotFoundError as error:
#         return error.output
#     except Exception as error:
#         return error.output


# def list_directory(path, extension=None):
#     if path_exists(path) == True:
#         files = os.listdir(path)
#         if extension:
#             filtered_files = [
#                 file
#                 for file in files
#                 if file.endswith(extension) and os.path.isfile(os.path.join(path, file))
#             ]
#             return filtered_files
#         else:
#             directory_files = [
#                 file for file in files if os.path.isfile(os.path.join(path, file))
#             ]
#             return directory_files
#     else:
#         return []


# def verify_command(command, grep=False):
#     try:
#         output = subprocess.run(
#             command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
#         )
#         return output
#     except Exception as e:
#         pass


# def verify_lsmod(module):
#     """
#     Checks if a kernel module is loaded.
#     :param module: The name of the module to check.
#     :return: True if the module is loaded, False otherwise.
#     """
#     lsmod_process = subprocess.Popen(["lsmod"], stdout=subprocess.PIPE, text=True)
#     grep_process = subprocess.Popen(
#         ["grep", module], stdin=lsmod_process.stdout, stdout=subprocess.PIPE, text=True
#     )
#     lsmod_process.stdout.close()
#     output = grep_process.communicate()[0]
#     return True if len(output) > 0 else False


# def verify_package(pkgmgr, package):
#     pkgmgr.append(package)
#     package_process = subprocess.Popen(
#         pkgmgr, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, text=True
#     )
#     grep_process = subprocess.Popen(
#         ["grep", package],
#         stdin=package_process.stdout,
#         stdout=subprocess.PIPE,
#         text=True,
#     )
#     package_process.stdout.close()
#     output = grep_process.communicate()[0]

#     if "installed" in output or len(output) > 0:
#         print(f"Package {package} installed")
#         return True
#     elif "not installed" in output or len(output) == 0:
#         print(f"Package {package} not installed")
#         return False


# def verify_service(cmd):
#     try:
#         output = subprocess.run(
#             cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
#         )
#         return output
#     except Exception as e:
#         pass
