import re

import sublime
import sublime_plugin

_MEMORY = []


# !! Renamed to "NextModification" from "BetterExpandScope"
# !! Why?  So that LSP's expand will default here
# !! Because 'ctrl+.' normally points at "next_modification"
class NextModificationCommand(sublime_plugin.TextCommand):
    def split_scope(self, pos):
        return re.findall(r"(?:^|\s+|\.)[^\s.]+", self.view.scope_name(pos))

    def find_by_selector_containing(self, selector, point):
        """Finds a region of text matching selector and containtaining point.

        Args:
            selector: a semantic description of the cursor's location
                (e.g., 'python.python-meta.function')
            point: the index of the editing cursor

        Returns:
            A <sublime.Region> matching selector and containing point.
        """
        return next(
            region
            for region in self.view.find_by_selector(selector)
            if region.contains(point)
        )

    def run(self, edit):
        selection = self.view.sel()
        new_lines_q = False

        # the region indeces needed in order to place cursor at start of region
        a_i = selection[0].a
        b_i = selection[0].b

        for region in selection:
            _MEMORY.append(region)
            expanded = self.get_expanded(region)
            if expanded and "\n" not in self.view.substr(expanded):
                selection.add(sublime.Region(expanded.b, expanded.a))
            else:
                new_lines_q = True

        if new_lines_q:
            selection.add(sublime.Region(selection[0].b, selection[0].a))

            # If selection is not bounded by brackets
            if (
                "{" not in self.view.substr(self.view.selection[0].a - 1)
                and "(" not in self.view.substr(self.view.selection[0].a - 1)
                and "[" not in self.view.substr(self.view.selection[0].a - 1)
            ):
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
        """Returns a <sublime.Region> that is strictly larger than the one passed in.

        Args:
            region: a small <sublime.Region>

        Returns:
            A larger <sublime.Region>

        Examples:
            >>> get_expanded(sublime.Region(100,200))
            <sublime.Region(99,201)>
        """
        target = self.split_scope(region.begin())  # starting index of passed selection
        while len(target):
            found = self.find_by_selector_containing("".join(target), region.begin())
            if found.contains(region) and not region.contains(found):
                return found
            else:
                target.pop()


class NarrowSelectionCommand(sublime_plugin.TextCommand):
    def split_scope(self, pos):
        return re.findall(r"(?:^|\s+|\.)[^\s.]+", self.view.scope_name(pos))

    def find_by_selector_containing(self, selector, point):
        return next(
            region
            for region in self.view.find_by_selector(selector)
            if region.contains(point)
        )

    def run(self, edit):
        selection = self.view.sel()

        if _MEMORY:
            old_selection = []
            for region in selection:
                memory = _MEMORY.pop()

                old_selection.append(memory)

            selection.clear()
            for region in old_selection:
                selection.add(region)

        else:
            for region in selection:
                expanded = self.get_narrow(region)
                # print(f"{expanded}")
                if expanded:
                    selection.clear()
                    selection.add(sublime.Region(expanded.a, expanded.b))

    def get_narrow(self, region):
        point = region.begin() + int(region.size() / 2)
        target = self.split_scope(point)  # middle index of passed selection
        prev = region
        while len(target):
            found = self.find_by_selector_containing("".join(target), point)
            if region.contains(found) and not found.contains(region):
                prev = found
                target.pop()
            else:
                return prev


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
