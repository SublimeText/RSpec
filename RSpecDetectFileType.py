import sublime, sublime_plugin
import os

class RSpecDetectFileTypeCommand(sublime_plugin.EventListener):
	'''
	Detects current file type if the file's extension isn't conclusive
	Modified for Ruby on Rails and Sublime Text 2
	Original pastie here: http://pastie.org/private/kz8gtts0cjcvkec0d4quqa
	'''

	def on_load(self, view):
		filename = view.file_name()

		if not filename: return # not saved

		name = os.path.basename(filename.lower())
		if name.endswith("_spec.rb"):
			set_syntax(view, "RSpec")
		elif name == "factories.rb":
			set_syntax(view, "RSpec")


def set_syntax(view, syntax, path=None):
	if path is None:
		path = syntax

	view.settings().set('syntax', 'Packages/'+ path + '/' + syntax + '.tmLanguage')
	print("Switched syntax to: " + syntax)
