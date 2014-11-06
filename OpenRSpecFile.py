import sublime
import sublime_plugin
import re, inspect, os
from RSpec import shared

class OpenRspecFileCommand(sublime_plugin.WindowCommand):

    def run(self):
        if not self.window.active_view():
            return

        current_file_path = self.window.active_view().file_name()

        if current_file_path.endswith(".rb"):
            current_file_name = re.search(r"[/\\]([\w.]+)$", current_file_path).group(1)
            base_name = re.search(r"(\w+)\.rb$", current_file_name).group(1)
            base_name = re.sub(r"_spec$", "", base_name)

            target_group = shared.other_group_in_pair(self.window)

            print("Current file: " + current_file_name)
            if current_file_name.endswith("_spec.rb"):
                source_matcher = re.compile(r"[/\\]" + base_name + "\.rb$")
                self.open_project_file(source_matcher, current_file_path, target_group)
            else:
                test_matcher = re.compile(r"[/\\]" + base_name + "_spec\.rb$")
                self.open_project_file(test_matcher, current_file_path, target_group)
        else:
            print("Error: current file is not a ruby file")

    def open_project_file(self, file_matcher, file_path, group):
        for path, dirs, filenames in self.walk_project_folder(file_path):
            for filename in filter(lambda f: f.endswith(".rb"), filenames):
                current_file = os.path.join(path, filename)
                if file_matcher.search(current_file):
                    file_view = self.window.open_file(os.path.join(path, filename))
                    self.window.run_command("move_to_group", { "group": group })
                    return print("Opened: " + filename)
        print("RSpec: No matching files found")

    def walk_project_folder(self, file_path):
        for folder in self.window.folders():
            if not file_path.startswith(folder):
                continue
            for dir_data in os.walk(folder):
                yield dir_data
