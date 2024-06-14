class Report:
    def __init__(self, title):
        self.title = title
        self.entries = []

    def add_entry(self, result):
        self.entries.append(result)

    def get_entries(self):
        return self.entries

    def generate_summary(self):
        summary = f"{self.title}\n" + "=" * len(self.title) + "\n"
        for entry in self.entries:
            summary + entry + "\n"
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
