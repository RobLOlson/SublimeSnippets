import sublime
import sublime_plugin


class FocusTabCommand(sublime_plugin.WindowCommand):
    def run(self, pos):
        self.window.focus_view(self.window.views()[pos])
