import sublime
import sublime_plugin
import pdb

import re

class BetterExpandSelectionCommand(sublime_plugin.TextCommand):
    def split_scope(self, pos):
        return re.findall(
            r'(?:^|\s+|\.)[^\s.]+',
            self.view.scope_name(pos)
        )

    def find_by_selector_containing(self, selector, point):
        return next(
            region
            for region in self.view.find_by_selector(selector)
            if region.contains(point)
        )

    def run(self, edit):
        selection = self.view.sel()
        for region in selection:
            expanded = self.get_expanded(region)
            if expanded: selection.add(expanded)

    def get_expanded(self, region):
        target = self.split_scope(region.begin())

        while len(target):
            found = self.find_by_selector_containing(''.join(target), region.begin())
            if found.contains(region) and not region.contains(found):
                print(''.join(target))
                return found
            else:
                target.pop()
