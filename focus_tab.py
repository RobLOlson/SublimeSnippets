"""Focus the current window on the tab in the Nth position."""

import sublime
import sublime_plugin


class FocusTabCommand(sublime_plugin.WindowCommand):
    """Focus the current window on the tab in position 'pos'."""

    def run(self, pos):
        """Hook for when the 'focus_tab' command is invoked."""
        self.window.focus_view(self.window.views()[pos])

    def test(self):
        """TEST"""
