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

        script_test_path = file_path.parent / "tests" / f"test_{file_path.name}"
        module_test_path = file_path.absolute().parent.parent / "tests" / f"test_{file_path.name}"

        if script_test_path.exists():
            view.window().run_command("exec", {"cmd": f"py -m pytest -s {script_test_path}"})

        if module_test_path.exists():
            view.window().run_command("exec", {"cmd": f"py -m pytest -s {module_test_path}"})
