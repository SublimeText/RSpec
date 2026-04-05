from typing import cast

import sublime
import sublime_plugin


class RspecTestCurrentLineCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if view is None:
            return

        file = view.file_name()
        if file is None:
            return

        rows = [view.rowcol(sel.a)[0] + 1 for sel in view.sel()]

        cwd: "str | None" = cast(
            str,
            sublime.expand_variables(
                r"${project_path:${folder:${file_path}}}",
                sublime.active_window().extract_variables(),
            ),
        )

        exec_args: sublime.CommandArgs = {
            "cmd": ["bundle", "exec", "rspec", f"{file}:{':'.join(map(str, rows))}"],
            "working_dir": cwd,
            "quiet": False,
        }

        self.window.run_command("exec", exec_args)

    def is_enabled(self):
        view = self.window.active_view()
        if view is None:
            return False

        syntax = view.syntax()
        return syntax is not None and syntax.scope == "source.ruby.rspec"
