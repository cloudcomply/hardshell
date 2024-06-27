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

    def set_result(
        self, check_id, check_name, check_result, check_subtype, check_type
    ) -> None:
        self.check_results.append(
            {
                "id": check_id,
                "name": check_name,
                "result": check_result,
                "subtype": check_subtype,
                "type": check_type,
            }
        )

        # click.echo(click.style("#" * 90, fg="blue"))
        # click.echo(click.style(f"# {self.category}", fg="blue"))

        for result in self.check_results:
            log_status(
                message=f"{result.get('id')} - {result.get('name')}",
                message_color="yellow",
                status=f"{result['result'].upper()}",
                status_color=("green" if result["result"] == "pass" else "red"),
            )
