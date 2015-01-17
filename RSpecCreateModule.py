import sublime, sublime_plugin, time
import re

from textwrap import dedent
from RSpec.shared import other_group_in_pair


def snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class GotoLineCommand(sublime_plugin.TextCommand):

    def run(self, edit, line, column=0):
        pt = self.view.text_point(line - 1, column)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt))

        self.view.show(pt)


class RspecNewModuleCommand(sublime_plugin.TextCommand):

    def run(self, edit, name, namespace):
        class_template = dedent('''
            class {name}

            end
        '''.lstrip('\n').rstrip(' \n').format(name=name))

        module_template = dedent('''
            module {module}
            {definition}
            end
        '''.lstrip('\n').rstrip(' \n'))

        template, level = class_template, len(namespace)

        while namespace:
            module = namespace.pop()
            template = module_template.format(module=module, definition=self.indent(template))

        self.view.insert(edit, 0, template)
        self.view.run_command('goto_line', { 'line': 2 + level, 'column': level * 2 })

    def indent(self, text, space=2):
        return '\n'.join(' ' * space + line for line in text.split('\n'))


class RspecNewSpecCommand(sublime_plugin.TextCommand):

    def run(self, edit, name):
        template = dedent('''
            require 'spec_helper'

            describe {name} do

            end
        '''.strip('\n').format(name=name))

        self.view.insert(edit, 0, template)
        self.view.run_command('goto_line', { 'line': 4 })


class RspecCreateModuleCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel("Enter module name:", "", self.on_done, None, None)

    def on_done(self, text):
        if not text: return

        *namespace, name = re.split(r'/|::', text.strip(' _/'))

        # create the module
        module = self.window.new_file()
        module.set_syntax_file('Packages/Ruby/Ruby.tmLanguage')
        module.set_name(snake_case(name) + '.rb')

        module.run_command('rspec_new_module', { 'name': name, 'namespace': namespace })

        # create the spec
        spec = self.window.new_file()
        self.window.run_command('move_to_group', { 'group': other_group_in_pair(self.window) })
        spec.set_syntax_file('Packages/Ruby/Ruby.tmLanguage')
        spec.set_name(snake_case(name) + '_spec.rb')

        spec.run_command('rspec_new_spec', { 'name': '::'.join(namespace + [name]) })
