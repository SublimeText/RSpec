import sublime
import sublime_plugin
import re, inspect, os
from RSpec import shared

class OpenRspecFileCommand(sublime_plugin.WindowCommand):

    def run(self):
        if not self.window.active_view():
            return

        current_file_path = self.window.active_view().file_name()
        print("Current file: " + current_file_path)

        if current_file_path.endswith(".rb"):
            if self.quick_find(current_file_path):
                return

            current_file_name = re.search(r"[/\\]([\w.]+)$", current_file_path).group(1)
            base_name = re.search(r"(\w+)\.rb$", current_file_name).group(1)
            base_name = re.sub(r"_spec$", "", base_name)

            if current_file_name.endswith("_spec.rb"):
                source_matcher = re.compile(r"[/\\]" + base_name + "\.rb$")
                self.open_project_file(source_matcher, current_file_path)
            else:
                test_matcher = re.compile(r"[/\\]" + base_name + "_spec\.rb$")
                self.open_project_file(test_matcher, current_file_path)
        else:
            print("Error: current file is not a ruby file")

    def open_project_file(self, file_matcher, file_path):
        for path, dirs, filenames in self.walk_project_folder(file_path):
            for filename in filter(lambda f: f.endswith(".rb"), filenames):
                current_file = os.path.join(path, filename)
                if file_matcher.search(current_file):
                    return self.switch_to(os.path.join(path, filename))
        print("RSpec: No matching files found")

    def quick_find(self, file_path):
        spec_regex = re.compile(r"\bspec\b")
        if re.search(r"\b(?:app|lib)\b", file_path):
            file_path = self.batch_replace(file_path,
                    (r"\b(?:app|lib)\b", "spec"), (r"\b(\w+)\.rb", r"\1_spec.rb"))
            if os.path.exists(file_path):
                return self.switch_to(file_path)
        elif spec_regex.search(file_path):
            file_path = re.sub(r"\b(\w+)_spec\.rb", r"\1.rb", file_path)
            for path in ["app", "lib"]:
                path = spec_regex.sub(path, file_path)
                if os.path.exists(path):
                    return self.switch_to(path)
        print("RSpec: quick find failed, doing regular find")

    def batch_replace(self, string, *pairs):
        for target, replacement in pairs:
            string = re.sub(target, replacement, string)
        return string

    def switch_to(self, file_path):
        group = shared.other_group_in_pair(self.window)
        file_view = self.window.open_file(file_path)
        self.window.run_command("move_to_group", { "group": group })
        print("Opened: " + file_path)
        return True

    def walk_project_folder(self, file_path):
        for folder in self.window.folders():
            if not file_path.startswith(folder):
                continue
            yield from os.walk(folder)
