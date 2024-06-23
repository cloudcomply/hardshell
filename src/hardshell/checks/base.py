from dataclasses import dataclass, field
from typing import List, Optional

from src.hardshell.common.logging import logger


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
