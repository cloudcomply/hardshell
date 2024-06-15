#########################################################################################
# Imports
#########################################################################################
from src.hardshell.report import Report
from src.hardshell.common.checks import create_checks
from src.hardshell.common.common import detect_os
from src.hardshell.common.config import GlobalConfig, load_config

# from src.hardshell.scanners.linux import audit_linux
# import subprocess


def start_scanner():
    detected_os = detect_os()
    if detected_os["type"] == "linux":
        # Config Setup
        global_config_path = "config/global.toml"
        checks_config_path = "config/linux.toml"

        global_config = GlobalConfig.from_toml(global_config_path)
        # global_config = load_config(global_config_path)
        checks_config = load_config(checks_config_path)
        # checks_config = Config.from_toml(checks_config_path)

        # print(global_config)
        # print(type(global_config))
        # print(checks_config)
        # print(type(checks_config))

        # Create Checks
        checks = create_checks(checks_config)

        # Create Report
        report = Report("Hardshell Report")

        # Run Checks
        for check in checks:
            check.run_check(current_os=detected_os, global_config=global_config)
            if check.check_results:
                print(f"Check: {check.check_name} - Result: {check.check_results}")
                report.add_entry(result=check.check_results)

    else:
        print("Unsupported OS")
        exit(1)


# Old Code

# global_config_path = "c:\\repos\\tom\\hardshell\\hardshell\\config\\global.toml"
# global_config_path = "config/global.toml"
# windows_config_path = "c:\\repos\\tom\\hardshell\\hardshell\\config\\linux.toml"
# linux_config_path = "config/linux.toml"

# global_config = load_config(global_config_path)
# linux_config = load_config(linux_config_path)

# for system_check in linux_config:
#     # print(linux_config[system_check])
#     for check in linux_config[system_check]:
#         print(linux_config[system_check][check]["check_name"])

# for check in checks:
#     print(
#         f"Category: {check}"
#         + " " * 5
#         + f"Total Checks {checks[check]['total']}"
#         + " " * 5
#         + f"Passed Checks {checks[check]['passed']}"
#         + " " * 5
#         + f"Failed Checks {checks[check]['failed']}"
#     )


# if check.check_result:
#     print(f"Check: {check.check_name} - Result: {check.check_result}")
#     report.add_entry(result=check.check_result)
# if check.result_service_active:
#     print(
#         f"Check: {check.check_name} - Service Active Result: {check.result_service_active}"
#     )
#     report.add_entry(result=check.result_service_active)
# if check.result_service_enabled:
#     print(
#         f"Check: {check.check_name} - Service Enabled Result: {check.result_service_enabled}"
#     )
#     report.add_entry(result=check.result_service_enabled)

# result = check.get_result()
# if result != None:
#     print(result)

# print(report.get_entries())
# report.export_to_txt("assessment_report.txt")
# report.export_to_html("assessment_report.html")

# audit_linux(
#     detected_os=detected_os,
#     global_config=global_config,
#     linux_config=linux_config,
# )

# print("-----------TESTING-----------")
# command = ["systemctl", "is-enabled", "cron2.service"]

# result = subprocess.run(
#     command,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
#     text=True,
#     # check=True,
# )

# print(f"result: {result}")

# output = result.stdout.strip()

# print(f"output: {output}")
