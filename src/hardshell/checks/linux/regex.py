import fnmatch
import glob
import os
import re
from dataclasses import dataclass, field
from typing import List

from distutils import log
from src.hardshell.checks.base import BaseCheck
from src.hardshell.common.common import get_config_mapping, log_and_print

# from src.hardshell.common.logging import


@dataclass
class RegexCheck(BaseCheck):
    file_ext: str = None
    ignore_case: bool = False
    multi_line: bool = False
    path: List[str] = field(default_factory=list)
    pattern: str = None
    pattern_match: bool = False

    def find_pattern_in_file(
        self, file_path, pattern, ignore_case=False, multi_line=False
    ):
        """
        Summary:
            Find a regex pattern in a file.

        Args:
            file_path (str): File path to search
            pattern (str): Regex pattern to match
            ignore_case (bool, optional): If True, ignore case. Defaults to False.
            multi_line (bool, optional): If True, treat the file as multi-line input. Defaults to False.

        Returns:
            bool: True if pattern was found, False otherwise.
        """
        # Regex pattern initial status
        pattern_found = False

        # Compile the pattern with the appropriate flags
        flags = 0
        if ignore_case:
            flags |= re.IGNORECASE
        if multi_line:
            flags |= re.MULTILINE

        log_and_print(f"Ignore Case Flag: {ignore_case}", log_only=True)
        log_and_print(f"Multi-line Flag: {multi_line}", log_only=True)
        log_and_print(f"Flags: {flags}", log_only=True)

        pattern = re.compile(pattern, flags)

        # Open and read the file
        log_and_print(f"Reading file: {file_path}", log_only=True)
        with open(file_path, "r") as file:
            content = file.read()
            if pattern.search(content):
                pattern_found = True

        log_and_print(f"Pattern found: {pattern_found}", log_only=True)
        return pattern_found

    def run_check(self, current_os, global_config):
        def search_file(file_path):
            log_and_print(f"Searching file: {file_path}", log_only=True)
            return self.find_pattern_in_file(
                file_path, self.pattern, self.ignore_case, self.multi_line
            )

        def search_in_directory(directory_path):
            log_and_print(f"Searching directory: {directory_path}", log_only=True)

            all_files = glob.glob(
                os.path.join(directory_path, "**", "*"), recursive=True
            )
            files = [
                file
                for file in all_files
                if os.path.isfile(file)
                and (
                    os.path.splitext(file)[1] == self.file_ext
                    if self.file_ext
                    else True
                )
            ]

            for file_path in files:
                if search_file(file_path):
                    return True
            return False

        log_and_print(f"Running Regex Check: {self.check_name}", log_only=True)

        # Log optional attributes if they exist
        for attribute, value in [
            ("File Extension", self.file_ext),
            ("Ignore Case", self.ignore_case),
            ("Multi-line", self.multi_line),
            ("Path", self.path),
            ("Pattern Match", self.pattern_match),
        ]:
            if value:
                log_and_print(f"{attribute}: {value}", log_only=True)

        pattern_found = False
        current_path = None

        if self.path is None and self.check_subtype is not None:
            log_and_print(
                f"Path not specified, using path from config mapping in global_config: {self.check_subtype}",
                log_only=True,
            )
            self.path = get_config_mapping(self.check_subtype, global_config)
            log_and_print(f"Global Config Path: {self.path}", log_only=True)

        paths = self.path if isinstance(self.path, list) else [self.path]

        log_and_print(f"Paths: {paths}", log_only=True)

        for path in paths:
            log_and_print(f"Path: {path}", log_only=True)
            current_path = path
            if os.path.isfile(path):
                log_and_print(
                    f"File: {path} is a file {os.path.isfile(path)}",
                    log_only=True,
                )
                if search_file(path):
                    log_and_print("search_file invoked", log_only=True)
                    pattern_found = True
                    break
            elif os.path.isdir(path):
                log_and_print(
                    f"Dir: {path} is a Dir {os.path.isdir(path)}",
                    log_only=True,
                )
                if search_in_directory(path):
                    log_and_print("search_in_directory invoked")
                    pattern_found = True
                    break
            else:
                log_and_print(f"Path {path} is not a file or directory", log_only=True)
                pattern_found = False

        found_status = "found" if pattern_found else "not found"
        match_status = (
            "and expected to find it."
            if self.pattern_match
            else "but not expected to find it."
        )
        path_description = (
            current_path
            # self.path
            # if isinstance(self.path, str) and os.path.isfile(self.path)
            # else "one of the files in the directory"
        )
        log_and_print(
            f"Pattern: {self.pattern} {found_status} in file: {path_description} {match_status}",
            log_only=True,
        )
        result = "pass" if pattern_found == self.pattern_match else "fail"
        self.set_result(
            self.check_id, self.check_name, result, "regex", self.check_type
        )
