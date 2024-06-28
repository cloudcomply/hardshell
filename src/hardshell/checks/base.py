from dataclasses import dataclass, field
import stat
from typing import List, Optional

import click

from src.hardshell.common.common import log_status


@dataclass
class BaseCheck:
    category: Optional[str] = None
    check_fail: List[str] = field(default_factory=list)
    check_id: Optional[str] = None
    check_name: Optional[str] = None
    check_pass: List[str] = field(default_factory=list)
    check_results: List[dict] = field(default_factory=list)
    check_subtype: Optional[str] = None
    check_type: Optional[str] = None
    depends_on: List[str] = field(default_factory=list)
    valid_os: List[str] = field(default_factory=list)

    def set_result_and_log_status(
        self,
        check_id=None,
        check_message=None,
        check_name=None,
        check_result=None,
        check_type=None,
        log_level="info",
        log_message=None,
        log_only=False,
    ) -> None:
        if check_result == "pass":
            status_color = "green"
        elif check_result == "skip":
            status_color = "yellow"
        else:
            status_color = "red"

        log_status(
            log_level=log_level,
            log_message=log_message,
            message=f"{check_id} - {check_name} - {check_message} - {check_type}",
            message_color="yellow",
            status=check_result,
            status_color=status_color,
            log_only=log_only,
        )

        if not log_only:
            self.check_results.append(
                {
                    "id": check_id,
                    "name": check_name,
                    "result": check_result,
                    "message": check_message,
                    "type": check_type,
                }
            )
