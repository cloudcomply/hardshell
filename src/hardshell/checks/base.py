from dataclasses import dataclass, field
from typing import List, Optional

import click

from src.hardshell.common.common import log_status


@dataclass
class BaseCheck:
    category: Optional[str] = None
    check_id: Optional[str] = None
    check_name: Optional[str] = None
    check_results: List[dict] = field(default_factory=list)
    check_pass: List[str] = field(default_factory=list)
    check_fail: List[str] = field(default_factory=list)
    check_subtype: Optional[str] = None
    check_type: Optional[str] = None
    depends_on: List[str] = field(default_factory=list)
    valid_os: List[str] = field(default_factory=list)

    def set_result_and_log_status(
        self, check_id, check_name, check_result, check_subtype, check_type
    ) -> None:
        log_status(
            message=f"{check_id} - {check_name} - {check_subtype} - {check_type}",
            message_color="yellow",
            status=check_result.upper(),
            status_color="green" if check_result == "pass" else "red",
        )
        self.check_results.append(
            {
                "id": check_id,
                "name": check_name,
                "result": check_result,
                "subtype": check_subtype,
                "type": check_type,
            }
        )
