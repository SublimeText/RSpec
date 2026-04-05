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


def snake_case(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


class GotoLineCommand(sublime_plugin.TextCommand):
    def run(self, edit, line, column: int=0) -> None:
        pt = self.view.text_point(line - 1, column)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt))

        self.view.show(pt)


class RspecNewModuleCommand(sublime_plugin.TextCommand):
    def run(self, edit, name, namespace) -> None:
        class_template = CLASS_TEMPLATE.format(name=name)

        template, level = class_template, len(namespace)

        while namespace:
            module = namespace.pop()
            template = MODULE_TEMPLATE.format(
                module=module, definition=self.indent(template)
            )

        self.view.insert(edit, 0, template)
        self.view.run_command("goto_line", {"line": 2 + level, "column": level * 2})

    def indent(self, text, space: int=2):
        return "\n".join(" " * space + line for line in text.split("\n"))


class RspecNewSpecCommand(sublime_plugin.TextCommand):
    def run(self, edit, name) -> None:
        template = SPEC_TEMPLATE.format(name=name)

        self.view.insert(edit, 0, template)
        self.view.run_command("goto_line", {"line": 4})


class RspecCreateModuleCommand(sublime_plugin.WindowCommand):
    def run(self) -> None:
        self.window.show_input_panel("Enter module name:", "", self.on_done, None, None)

    def on_done(self, text) -> None:
        if not text:
            return

        *namespace, name = re.split(r"/|::", text.strip(" _/"))

        # create the module
        module = self.window.new_file(syntax="scope:source.ruby")
        module.set_name(snake_case(name) + ".rb")

        module.run_command("rspec_new_module", {"name": name, "namespace": namespace})

        # create the spec
        spec = self.window.new_file(syntax="scope:source.ruby.rspec")
        self.window.run_command(
            "move_to_group", {"group": other_group_in_pair(self.window)}
        )
        spec.set_name(snake_case(name) + "_spec.rb")

        spec.run_command("rspec_new_spec", {"name": "::".join(namespace + [name])})
