import re

import sublime
import sublime_plugin

_MEMORY = []

# Renamed "NextModification" from "BetterExpandScope"
# Why?  So that LSP's expand will default here
# Because 'ctrl+.' normally points at "next_modification"
class NextModificationCommand(sublime_plugin.TextCommand):
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
        new_lines_q = False
        a_i = selection[0].a
        b_i = selection[0].b

        # global _MEMORY

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
        target = self.split_scope(region.begin())  # starting index of passed selection
        while len(target):
            found = self.find_by_selector_containing("".join(target), region.begin())
            if found.contains(region) and not region.contains(found):
                return found
            else:
                target.pop()

                class NextModificationCommand(sublime_plugin.TextCommand):
                    def split_scope(self, pos):
                        return re.findall(
                            r"(?:^|\s+|\.)[^\s.]+", self.view.scope_name(pos)
                        )

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

                        print(f"{self.__class__}")

                        for region in selection:
                            expanded = self.get_expanded(region)
                            if expanded and "\n" not in self.view.substr(expanded):
                                selection.add(sublime.Region(expanded.b, expanded.a))
                            else:
                                new_lines_q = True

                        if new_lines_q:
                            selection.add(
                                sublime.Region(selection[0].b, selection[0].a)
                            )

                            # If selection is not bounded by brackets
                            if (
                                "{"
                                not in self.view.substr(self.view.selection[0].a - 1)
                                and "("
                                not in self.view.substr(self.view.selection[0].a - 1)
                                and "["
                                not in self.view.substr(self.view.selection[0].a - 1)
                            ):
                                self.view.run_command(
                                    "expand_selection", {"to": "indentation"}
                                )
                            self.view.run_command(
                                "expand_selection", {"to": "brackets"}
                            )
                            selection.add(
                                sublime.Region(selection[0].b, selection[0].a)
                            )

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
                                selection.add(
                                    sublime.Region(selection[0].a, selection[0].b)
                                )

                    def get_expanded(self, region):
                        target = self.split_scope(
                            region.xpos
                        )  # starting index of passed selection
                        while len(target):
                            found = self.find_by_selector_containing(
                                "".join(target), region.begin()
                            )
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
            memory = _MEMORY.pop()

            selection.clear()
            selection.add(memory)

        else:
            for region in selection:
                expanded = self.get_expanded(region)
                # print(f"{expanded}")
                if expanded:
                    selection.clear()
                    selection.add(sublime.Region(expanded.a, expanded.b))

    def get_expanded(self, region):
        point = region.begin() + int(region.size() / 2)
        target = self.split_scope(point)  # middle index of passed selection
        prev = region
        while len(target):
            found = self.find_by_selector_containing("".join(target), point)
            if region.contains(found) and not found.contains(region):
                prev = found
                target.pop()
            else:
                print(f"{found=}")
                return prev
                return found


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
