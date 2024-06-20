from dataclasses import dataclass, field
from typing import List, Optional


class BaseCheck:
    def __init__(
        self,
        category: Optional[str],
        check_id: Optional[str],
        check_name: Optional[str],
        # check_results: List[str],
        check_subtype: Optional[str],
        check_type: Optional[str],
        depends_on: Optional[List[str]],
        valid_os: Optional[List[str]],
    ):
        self.category = category
        self.check_id = check_id
        self.check_name = check_name
        # self.check_results = check_results
        self.check_subtype = check_subtype
        self.check_type = check_type
        self.depends_on = depends_on
        self.valid_os = valid_os
