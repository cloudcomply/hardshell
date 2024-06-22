from dataclasses import dataclass, field
from typing import List
from src.hardshell.common.logging import logger


@dataclass
class Report:
    title: str = None
    entries: List[int] = field(default_factory=list)

    def add_entry(self, result):
        self.entries.append(result)

    def get_entries(self):
        return self.entries

    def generate_summary(self):
        checks_passed = 0
        checks_failed = 0
        summary = f"{self.title}\n" + "=" * len(self.title) + "\n"
        for entry in self.entries:
            if entry.get("result") == "pass":
                checks_passed += 1
            else:
                checks_failed += 1

            summary += (
                f"Check Name: {str(entry.get('name'))}"
                + "\t"
                + f"Check ID: {str(entry.get('id'))}"
                + "\t"
                + f"Check Type: {str(entry.get('type'))}"
                + "\t"
                + f"Check Subtype: {str(entry.get('subtype'))}"
                + "\t"
                + f"Check Result: {str(entry.get('result'))}"
                + "\n"
            )

        summary += f"\nChecks passed: {checks_passed}\nChecks failed: {checks_failed}\n"

        return summary

    def export_to_txt(self, file_path):
        with open(file_path, "w") as file:
            file.write(self.generate_summary())

    def export_to_html(self, file_path):
        html_content = f"<html><head><title>{self.title}</title></head><body>"
        html_content += f"<h1>{self.title}</h1><ul>"
        for entry in self.entries:
            html_content += f"<li>{entry}</li>"
        html_content += "</ul></body></html>"
        with open(file_path, "w") as file:
            file.write(html_content)
