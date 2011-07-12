import sublime, sublime_plugin, time
import re

_patterns = dict((k, re.compile('_*' + v)) for (k, v)
                    in dict(allcamel=r'(?:[A-Z]+[a-z0-9]*)+$',
                            trailingcamel=r'[a-z]+(?:[A-Z0-9]*[a-z0-9]*)+$',
                            underscores=r'(?:[a-z]+_*)+[a-z0-9]+$').iteritems())

_caseTransition = re.compile('([A-Z][a-z]+)')

def translate(name, _from, to):
    leading_underscores = str()
    while name[0] == '_':
        leading_underscores += '_'
        name = name[1:]

    if _from in ('allcamel', 'trailingcamel'):
        words = _caseTransition.split(name)
    else:
        words = name.split('_')

    words = list(w for w in words if w is not None and 0 < len(w))

    camelize = lambda words: ''.join(w[0].upper() + w[1:] for w in words)

    v = dict(smushed=lambda: ''.join(words).lower(),
             allcamel=lambda: camelize(words),
             trailingcamel=lambda: words[0].lower() + camelize(words[1:]),
             underscores=lambda: '_'.join(words).lower())[to]()

    return leading_underscores + v


class RspecCreateModuleCommand(sublime_plugin.WindowCommand):
	def run(self):
		# self.view.insert(edit, 0, "Hello, World!")
		self.window.show_input_panel("Enter module name:", "", self.on_done, None, None)
	
	def on_done(self, text):

		# configure 2-paned layout (spec, module)
		self.window.run_command('set_layout', {
			"cols": [0.0, 0.5, 1.0],
			"rows": [0.0, 1.0],
			"cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
		})
		
		# create the spec
		spec = self.window.new_file()
		self.window.run_command('move_to_group', {'group': 0})
		spec.set_syntax_file('Packages/Ruby/Ruby.tmLanguage')
		spec.set_name(translate(text, 'allcamel', 'underscores') + '_spec.rb')
		spec_template = "require 'spec_helper'\n\
require '" + translate(text, 'allcamel', 'underscores') + "'\n\n\
describe " + text + " do\n\
\tit \"should do something\"\n\
end"
		edit = spec.begin_edit()
		spec.insert(edit, 0, spec_template)
		spec.end_edit(edit)

		# create the module
		module = self.window.new_file()
		self.window.run_command('move_to_group', {'group': 1})
		module.set_syntax_file('Packages/Ruby/Ruby.tmLanguage')
		module.set_name(translate(text, 'allcamel', 'underscores') + '.rb')
		module_template = "\n\
class " + text + "\n\
end"
		edit = module.begin_edit()
		module.insert(edit, 0, module_template)
		module.end_edit(edit)
		# try:
		# except ValueError:
		#     pass