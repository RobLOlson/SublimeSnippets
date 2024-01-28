from pathlib import Path

import sublime
import sublime_plugin


class AutoRunPytestOnSave(sublime_plugin.EventListener):
    """A class to listen for events triggered by ST."""

    def on_post_save_async(self, view):
        """Run pytest for the current *.py file when it is saved."""

        file_path = Path(view.file_name())

        if not file_path or file_path.suffix != ".py":
            return

        test_path = file_path.parent / "tests" / f"test_{file_path.name}"

        if test_path.exists():
            view.window().run_command("exec", {"cmd": f"py -m pytest -s {test_path}"})
