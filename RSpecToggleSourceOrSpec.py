import os
import re
from pathlib import Path
from typing import Iterator, cast

import sublime
import sublime_plugin

from . import shared


class RspecToggleSourceOrSpecCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if not view:
            return

        current_file_path = view.file_name()
        if current_file_path is None:
            return

        if self.quick_find(current_file_path):
            return

        path = Path(current_file_path)
        current_file_name = path.name
        base_name = path.stem

        if current_file_name.endswith("_spec.rb"):
            base_name = re.sub(r"_spec$", "", base_name)
            target = base_name + ".rb"
            self.open_project_file(target, current_file_path)
        else:
            target = base_name + "_spec.rb"
            self.open_project_file(target, current_file_path)

    def open_project_file(self, target: "str", file_path: str):
        excluded = cast(
            "list[str]",
            sublime.load_settings("Preferences.sublime-settings").get(
                "folder_exclude_patterns"
            ),
        )
        for path, dirs, filenames in self.walk_project_folder(file_path):
            dirs[:] = [d for d in dirs if d not in excluded]
            if target in filenames:
                return self.switch_to(os.path.join(path, target))
        print("RSpec: No matching files found")

    def spec_paths(self, file_path: str):
        return [
            self.batch_replace(
                file_path, (r"\b(?:app|lib)\b", "spec"), (r"\b(\w+)\.rb", r"\1_spec.rb")
            ),
            self.batch_replace(
                file_path,
                (r"\blib\b", os.path.join("spec", "lib")),
                (r"\b(\w+)\.rb", r"\1_spec.rb"),
            ),
        ]

    def code_paths(self, file_path: str):
        file_path = re.sub(r"\b(\w+)_spec\.rb$", r"\1.rb", file_path)
        return [
            re.sub(r"\bspec\b", "app", file_path),
            re.sub(r"\bspec\b", "lib", file_path),
            re.sub(r"\b{}\b".format(os.path.join("spec", "lib")), "lib", file_path),
        ]

    def quick_find(self, file_path: str) -> bool:
        """Guesses location of the target based on common Ruby project layouts

        SIDE EFFECT: Opens/focuses a file

        Returns a boolean representing whether or not the file was found"""
        if re.search(r"\bspec\b|_spec\.rb$", file_path):
            for path in self.code_paths(file_path):
                if os.path.exists(path):
                    return self.switch_to(path)
        elif re.search(r"\b(?:app|lib)\b", file_path):
            for path in self.spec_paths(file_path):
                if os.path.exists(path):
                    return self.switch_to(path)
        print("RSpec: quick find failed, doing regular find")
        return False

    def batch_replace(self, string: str, *pairs: "tuple[str, str]") -> str:
        for target, replacement in pairs:
            string = re.sub(target, replacement, string)
        return str(string)

    def switch_to(self, file_path: str):
        group = shared.other_group_in_pair(self.window)
        self.window.open_file(file_path)
        self.window.run_command("move_to_group", {"group": group})
        print("Opened: " + file_path)
        return True

    def walk_project_folder(
        self, file_path: str
    ) -> "Iterator[tuple[str, list[str], list[str]]]":
        for folder in self.window.folders():
            if not file_path.startswith(folder):
                continue
            yield from os.walk(folder)

    def is_enabled(self):
        view = self.window.active_view()
        return view is not None and self._is_ruby_file(view)

    def _is_ruby_file(self, view: sublime.View) -> bool:
        syntax = view.syntax()
        return syntax is not None and syntax.scope in (
            "source.ruby",
            "source.ruby.rspec",
        )
