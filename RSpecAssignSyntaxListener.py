import sublime
import sublime_plugin


class RSpecAssignSyntaxListener(sublime_plugin.EventListener):
    """Assigns the package's RSpec syntax to Ruby files matching common patterns"""

    def on_load(self, view: sublime.View) -> None:
        filename = view.file_name()

        if not filename:
            return  # not saved

        syntax = view.syntax()
        if syntax and syntax.scope == "source.ruby":
            if filename.endswith("_spec.rb"):
                view.assign_syntax("scope:source.ruby.rspec")
