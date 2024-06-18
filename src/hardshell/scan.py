#########################################################################################
# Imports
#########################################################################################
from src.hardshell.report import Report
from src.hardshell.common.checks import create_checks
from src.hardshell.common.common import detect_os
from src.hardshell.common.config import GlobalConfig, load_config

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
