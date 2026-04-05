import sublime
import sublime_plugin


class RspecGenerateSpecificationCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if view is None:
            return

        symbols = view.symbol_regions()
        result: list[str] = []
        for symbol in symbols:
            # Sublime automatically assigns NAMESPACE for "RSpec.describe" format
            # https://github.com/sublimehq/sublime_text/issues/3315
            if symbol.kind[0] in (sublime.KindId.KEYWORD, sublime.KindId.NAMESPACE):
                result.append(symbol.name)

        doc_file = self.window.new_file()
        doc_file.set_name("RSpec specification")
        doc_file.set_scratch(True)
        doc_file.run_command("rspec_insert_content", {"text": "\n".join(result)})

    def is_enabled(self):
        view = self.window.active_view()
        if view is None:
            return False

        syntax = view.syntax()
        return syntax is not None and syntax.scope == "source.ruby.rspec"
