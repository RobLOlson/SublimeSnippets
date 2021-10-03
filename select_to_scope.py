import re

import sublime
import sublime_plugin


class BetterExpandSelectionCommand(sublime_plugin.TextCommand):
    def split_scope(self, pos):
        return re.findall(r'(?:^|\s+|\.)[^\s.]+', self.view.scope_name(pos))

    def find_by_selector_containing(self, selector, point):
        return next(
            region
            for region in self.view.find_by_selector(selector)
            if region.contains(point)
        )

    def run(self, edit):
        selection = self.view.sel()
        new_lines_q = False
        a_i = selection[0].a
        b_i = selection[0].b

        for region in selection:
            expanded = self.get_expanded(region)
            if expanded and "\n" not in self.view.substr(expanded):
                selection.add(sublime.Region(expanded.b, expanded.a))
            else:
                new_lines_q = True

        if new_lines_q:
            selection.add(sublime.Region(selection[0].b, selection[0].a))

            # If selection is not bounded by brackets
            if "{" not in self.view.substr(self.view.selection[0].a-1) and \
               "(" not in self.view.substr(self.view.selection[0].a-1) and \
               "[" not in self.view.substr(self.view.selection[0].a-1):
                self.view.run_command("expand_selection", {"to": "indentation"})
            self.view.run_command("expand_selection", {"to": "brackets"})
            selection.add(sublime.Region(selection[0].b, selection[0].a))

            if abs(a_i - b_i) == abs(selection[0].a - selection[0].b):
                self.view.run_command(
                    "move",
                    {
                        "by": "stops",
                        "empty_line": True,
                        "extend": True,
                        "forward": False,
                    },
                )
                selection.add(sublime.Region(selection[0].a, selection[0].b))

    def get_expanded(self, region):
        target = self.split_scope(region.begin())  # starting index of passed selection
        while len(target):
            found = self.find_by_selector_containing(''.join(target), region.begin())
            if found.contains(region) and not region.contains(found):
                return found
            else:
                target.pop()


# Original Version
#
#     def split_scope(self, pos):
#         return re.findall(
#             r'(?:^|\s+|\.)[^\s.]+',
#             self.view.scope_name(pos)
#         )

#     def find_by_selector_containing(self, selector, point):
#         return next(
#             region
#             for region in self.view.find_by_selector(selector)
#             if region.contains(point)
#         )

#     def run(self, edit):
#         selection = self.view.sel()
#         for region in selection:
#             expanded = self.get_expanded(region)
#             if expanded: selection.add(expanded)

#     def get_expanded(self, region):
#         target = self.split_scope(region.begin())

#         while len(target):
#             found = self.find_by_selector_containing(''.join(target), region.begin())
#             if found.contains(region) and not region.contains(found):
#                 return found
#             else:
#                 target.pop()
