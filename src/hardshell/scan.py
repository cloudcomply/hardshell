#########################################################################################
# Imports
#########################################################################################
import platform

import click

from src.hardshell.common.checks import create_checks
from src.hardshell.common.common import (
    detect_admin,
    detect_os,
    log_and_print,
    shutdown_banner,
    startup_banner,
)
from src.hardshell.common.config import GlobalConfig, load_config
from src.hardshell.common.report import Report


def start_scanner():
    click.echo(click.style("Starting Scanner", fg="blue"))
    detected_os = detect_os()
    banner_startup = startup_banner(detected_os)

    click.echo(click.style("\n".join(banner_startup), fg="blue"))

    if detect_admin():
        if detected_os["type"] == "linux":
            # Config Setup
            global_config_path = "config/global.toml"
            checks_config_path = "config/linux.toml"

            global_config = GlobalConfig.from_toml(global_config_path)
            # global_config = load_config(global_config_path)
            checks_config = load_config(checks_config_path)
            # checks_config = Config.from_toml(checks_config_path)

            # Create Checks
            checks = create_checks(checks_config, current_os=detected_os)

            # Create Report
            report = Report("hardshell report")

            # Run Checks
            for check in checks:
                log_and_print(
                    f"running {check.check_type} check: {check.check_name}",
                    log_only=True,
                )

                # click.echo(click.style("#" * 90, fg="blue"))

                check.run_check(current_os=detected_os, global_config=global_config)
                if check.check_results:
                    # log_and_print(
                    #     f"check: {check.check_name} - result: {check.check_results}"
                    # )
                    for result in check.check_results:
                        report.add_entry(result=result)

            # Formatted Results
            report.get_check_results_total_formatted()

            # Check Report
            report.export_to_txt("report.txt")

        else:
            log_and_print("unsupported os")
            exit(1)
    else:
        log_and_print("must be admin")
        exit(1)
