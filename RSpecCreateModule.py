import re

import sublime
import sublime_plugin

from .shared import other_group_in_pair

CLASS_TEMPLATE = """\
class {name}

end"""

MODULE_TEMPLATE = """\
module {module}
{definition}
end"""

SPEC_TEMPLATE = """\
require 'spec_helper'

describe {name} do

end
"""


def indent(text: str, space: int = 2):
    return "\n".join(" " * space + line for line in text.split("\n"))


def snake_case(name: str):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


class RspecGotoLineAndIndentCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, line: int = 0, column: int = 0):
        pt = self.view.text_point(line - 1, column)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt))

        self.view.show(pt)
        self.view.insert(edit, pt, "  ")

    def is_visible(self):
        return False


class RspecCreateModuleCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Enter module name:", "", self.on_done, None, None)

    def on_done(self, text: str):
        if not text:
            return

        *namespace, name = re.split(r"/|::", text.strip(" _/"))

        # create the module
        module = self.window.new_file(syntax="scope:source.ruby")
        module.set_name(snake_case(name) + ".rb")
        module_template = CLASS_TEMPLATE.format(name=name)
        for mod in reversed(namespace):
            module_template = MODULE_TEMPLATE.format(
                module=mod, definition=indent(module_template)
            )
        module.run_command("rspec_insert_content", {"text": module_template})
        module.run_command(
            "rspec_goto_line_and_indent",
            {"line": 2 + len(namespace), "column": len(namespace) * 2},
        )

        # create the spec
        spec = self.window.new_file(syntax="scope:source.ruby.rspec")
        self.window.run_command(
            "move_to_group", {"group": other_group_in_pair(self.window)}
        )
        spec.set_name(snake_case(name) + "_spec.rb")
        self.window.run_command(
            "move_to_group", {"group": other_group_in_pair(self.window)}
        )
        spec.set_name(snake_case(name) + "_spec.rb")
        spec.run_command(
            "rspec_insert_content",
            {"text": SPEC_TEMPLATE.format(name="::".join(namespace + [name]))},
        )
        spec.run_command("rspec_goto_line_and_indent", {"line": 4})
