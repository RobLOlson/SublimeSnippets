import sublime_plugin


class SelectExactMatchCommand(sublime_plugin.TextCommand):
    last_selection = None

    def run(self, edit):
        selections = self.view.sel()
        words_selection = False
        for selection in selections:
            if selection.empty():
                words_selection = True
                region = self.view.word(selection)
                selections.add(region)
                self.view.show(region)
        if words_selection:
            return
        word = self.view.substr(self.view.word(selections[-1]))
        pattern = "\\b%s\\b" % (word)
        region = self.view.find(pattern, selections[-1].end())
        if not region:
            region = self.view.find(
                pattern, self.last_selection.end() if self.last_selection else 0
            )
            if region:
                self.last_selection = region
        else:
            self.last_selection = None
        if region:
            selections.add(region)
            self.view.show(region)


class SelectAllExactMatchesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selections = self.view.sel()
        if selections[-1].empty():
            selections.add(self.view.word(selections[-1]))
        word = self.view.substr(self.view.word(selections[-1]))
        pattern = "\\b%s\\b" % (word)
        selections.add_all(self.view.find_all(pattern))

    def description():
        return "Select All Exact Matches"
