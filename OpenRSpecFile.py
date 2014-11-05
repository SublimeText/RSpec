import sublime
import sublime_plugin
import re, inspect, os
from RSpec import shared

class OpenRspecFileCommand(sublime_plugin.WindowCommand):

    def run(self):
        if not self.window.active_view(): return

        current_file_path = self.window.active_view().file_name()

        if re.search(r"\w+\.rb$", current_file_path):
            current_file_name = re.search(r"[/\\]([\w.]+)$", current_file_path).group(1)
            base_name = re.search(r"(\w+)\.rb$", current_file_name).group(1)
            base_name = re.sub(r"_spec$", "", base_name)

            target_group = shared.other_group_in_pair(self.window)

            print("Current file: " + current_file_name)
            if current_file_name.endswith("_spec.rb"):
                source_matcher = re.compile(r"[/\\]" + base_name + "\.rb$")
                self.open_project_file(source_matcher, target_group)
            elif current_file_name.endswith(".rb"):
                test_matcher = re.compile(r"[/\\]" + base_name + "_spec\.rb$")
                self.open_project_file(test_matcher, target_group)
            else:
                print("Error: current file is not valid for RSpec to switch file")
        else:
            print("Error: current file is not a ruby file")

    def open_project_file(self, file_matcher, group):
        for path, dirs, filenames in self.walk_all_folders():
            for filename in filter(lambda f: f.endswith(".rb"), filenames):
                current_file = os.path.join(path, filename)
                if file_matcher.search(current_file):
                    file_view = self.window.open_file(os.path.join(path, filename))
                    self.window.run_command("move_to_group", { "group": group })
                    return print("Opened: " + filename)
        print("RSpec: No matching files found")

    def walk_all_folders(self):
        for folder in self.window.folders():
            yield from os.walk(folder)
