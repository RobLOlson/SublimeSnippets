import sublime
import sublime_plugin


class AutoRunPytestOnSave(sublime_plugin.EventListener):
    """A class to listen for events triggered by ST."""

    def on_post_save_async(self, view):
        """
        This is called after a view has been saved. It runs in a separate thread
        and does not block the application.
        """

        file_path = view.file_name()
        if not file_path:
            return
        NOT_FOUND = -1
        pos_dot = file_path.rfind(".")
        if pos_dot == NOT_FOUND:
            return
        file_extension = file_path[pos_dot:]
        if file_extension.lower() in [".py"]:
            # view.window().run_command("eslint")
            view.window().run_command("exec", {"cmd": "py -m pytest -s"})
