import sublime
import sublime_plugin
import re, inspect, os

class OpenRspecFileCommand(sublime_plugin.WindowCommand):

	def run(self, option):
		if not self.window.active_view():
			return

		self.views = []
		window = self.window
		current_file_path = self.window.active_view().file_name()

		if re.search(r"\w+\.rb$", current_file_path):
			
			current_file = re.search(r"([\w\.]+)$", current_file_path).group(1)
			base_name = re.search(r"(\w+)\.(\w+)$", current_file).group(1)
			base_name = re.sub('_spec', '', base_name)

			source_matcher = re.compile("[/\\\\]" + base_name + "\.rb$")
			test_matcher   = re.compile("[/\\\\]" + base_name + "_spec\.rb$")

			if option == 'next':
				print "Current file: " + current_file
				if  re.search(re.compile(base_name + "_spec\.rb$"), current_file):
					self.open_project_file(source_matcher, window)
				elif re.search(re.compile(base_name + "\.rb$"), current_file):
					self.open_project_file(test_matcher, window)
				else:
					print "Current file is not valid for RSpec switch file!"
			elif option == 'source':
				self.open_project_file(source_matcher, window)
			elif option == 'test':
				self.open_project_file(test_matcher, window)
			elif option == 'test_and_source':
				window.run_command('set_layout', {
                            "cols": [0.0, 0.5, 1.0],
                            "rows": [0.0, 1.0],
                            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
                        })
				self.open_project_file(test_matcher, window, 0)
				self.open_project_file(source_matcher, window, 1)
			
		for v in self.views:
			window.focus_view(v)
				
	def open_project_file(self, file_matcher, window, auto_set_view=-1):
		for root, dirs, files in os.walk(window.folders()[0]):
			for f in files:
				if re.search(r"\.rb$", f):
					cur_file = os.path.join(root, f)
					# print "Assessing: " + cur_file
					if file_matcher.search(cur_file):
						file_view = window.open_file(os.path.join(root, f))
						if auto_set_view >= 0: # don't set the view unless specified
							window.run_command('move_to_group', {'group': auto_set_view})
						self.views.append(file_view)
						print("Opened: " + f)
						return
		print("No matching files!")
