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

    def spec_paths(self, file_path: str) -> "list[str]":
        path = Path(file_path)
        target = path.stem + "_spec.rb"
        guesses = (
            self.swap_segment(path, ("lib",), ("spec", "lib")),
            self.swap_segment(path, ("app",), ("spec",)),
            self.swap_segment(path, ("lib",), ("spec",)),
        )
        return [str(guess.with_name(target)) for guess in guesses if guess]

    def code_paths(self, file_path: str) -> "list[str]":
        path = Path(file_path)
        target = re.sub(r"_spec$", "", path.stem) + ".rb"
        guesses = (
            self.swap_segment(path, ("spec", "lib"), ("lib",)),
            self.swap_segment(path, ("spec",), ("app",)),
            self.swap_segment(path, ("spec",), ("lib",)),
        )
        return [str(guess.with_name(target)) for guess in guesses if guess]

    def swap_segment(
        self, path: Path, old: "tuple[str, ...]", new: "tuple[str, ...]"
    ) -> "Path | None":
        """Replaces the first run of directory components matching `old` with `new`"""
        parts = path.parts
        for i in range(len(parts) - len(old)):  # the bound excludes the filename
            if parts[i : i + len(old)] == old:
                return Path(*parts[:i], *new, *parts[i + len(old) :])
        return None

    def quick_find(self, file_path: str) -> bool:
        """Guesses location of the target based on common Ruby project layouts

        SIDE EFFECT: Opens/focuses a file

        Returns a boolean representing whether or not the file was found"""
        path = Path(file_path)
        if path.name.endswith("_spec.rb") or "spec" in path.parts[:-1]:
            guesses = self.code_paths(file_path)
        else:
            guesses = self.spec_paths(file_path)
        for guess in guesses:
            if os.path.exists(guess):
                return self.switch_to(guess)
        print("RSpec: quick find failed, doing regular find")
        return False

    def switch_to(self, file_path: str):
        group = shared.other_group_in_pair(self.window)
        self.window.open_file(file_path)
        self.window.run_command("move_to_group", {"group": group})
        print("Opened: " + file_path)
        return True

    def walk_project_folder(
        self, file_path: str
    ) -> "Iterator[tuple[str, list[str], list[str]]]":
        norm_file = os.path.normcase(file_path)
        for folder in self.window.folders():
            # the trailing separator keeps a folder from matching a sibling it prefixes
            prefix = os.path.normcase(folder).rstrip(os.sep) + os.sep
            if not norm_file.startswith(prefix):
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
