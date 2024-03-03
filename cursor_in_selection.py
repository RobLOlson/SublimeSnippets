import sublime
import sublime_plugin


class MoveCursorToTenthInSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.sel()[0]:
            self.view.run_command("expand_selection", {"to": "line"})

        for region in self.view.sel():
            if region.empty():  # If single cursor, no need to move
                continue
            middle_point = region.a + (region.size() / 10)
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(middle_point))


class MoveCursorToTwentiethInSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.sel()[0]:
            self.view.run_command("expand_selection", {"to": "line"})

        for region in self.view.sel():
            if region.empty():  # If single cursor, no need to move
                continue
            middle_point = region.a + (region.size() / 10) * 2
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(middle_point))


class MoveCursorToThirtiethInSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.sel()[0]:
            self.view.run_command("expand_selection", {"to": "line"})

        for region in self.view.sel():
            if region.empty():  # If single cursor, no need to move
                continue
            middle_point = region.a + (region.size() / 10) * 3
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(middle_point))


class MoveCursorToFortiethInSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.sel()[0]:
            self.view.run_command("expand_selection", {"to": "line"})

        for region in self.view.sel():
            if region.empty():  # If single cursor, no need to move
                continue
            middle_point = region.a + (region.size() / 10) * 4
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(middle_point))


class MoveCursorToFiftiethInSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.sel()[0]:
            self.view.run_command("expand_selection", {"to": "line"})

        for region in self.view.sel():
            if region.empty():  # If single cursor, no need to move
                continue
            middle_point = region.a + (region.size() / 10) * 5
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(middle_point))


class MoveCursorToSixtiethInSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.sel()[0]:
            self.view.run_command("expand_selection", {"to": "line"})

        for region in self.view.sel():
            if region.empty():  # If single cursor, no need to move
                continue
            middle_point = region.a + (region.size() / 10) * 6
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(middle_point))


class MoveCursorToSeventiethInSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.sel()[0]:
            self.view.run_command("expand_selection", {"to": "line"})

        for region in self.view.sel():
            if region.empty():  # If single cursor, no need to move
                continue
            middle_point = region.a + (region.size() / 10) * 7
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(middle_point))


class MoveCursorToEightiethInSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.sel()[0]:
            self.view.run_command("expand_selection", {"to": "line"})

        for region in self.view.sel():
            if region.empty():  # If single cursor, no need to move
                continue
            middle_point = region.a + (region.size() / 10) * 8
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(middle_point))


class MoveCursorToNinetiethInSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.sel()[0]:
            self.view.run_command("expand_selection", {"to": "line"})

        for region in self.view.sel():
            if region.empty():  # If single cursor, no need to move
                continue

            middle_point = region.a + (region.size() / 10) * 9
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(middle_point))


class JumpToNextCharCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view

        def on_character(character):
            if len(character) != 1:
                sublime.status_message("Please enter a single character")
                return

            current_region = view.sel()[0]
            next_region = view.find(character, current_region.end())

            if next_region:
                view.sel().clear()
                view.sel().add(next_region)
                view.show(next_region)
            else:
                sublime.status_message("Character not found")

        view.window().show_input_panel("Press the character to find:", "", on_character, None, None)
