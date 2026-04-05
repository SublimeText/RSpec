import sublime
import sublime_plugin


def other_group_in_pair(window):
    """Returns the neighbour focus group for the current window."""
    if window.active_group() % 2 == 0:
        target_group = window.active_group() + 1
    else:
        target_group = window.active_group() - 1
    return min(target_group, window.num_groups() - 1)


# TODO: Call from RspecNewModuleCommand and RspecNewSpecCommand
class RspecInsertContentCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, text: str = ""):
        self.view.insert(edit, 0, text)
