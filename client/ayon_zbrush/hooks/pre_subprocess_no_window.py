import subprocess

from ayon_applications import PreLaunchHook, LaunchTypes
from ayon_core.lib import is_using_ayon_console


class LaunchServerNoWindow(PreLaunchHook):
    """Launch the AYON server of ZBrush without its own console window.

    The server is a separate process that prints its logs and tracebacks to
    the console. Its output is not accessible without a console, which makes
    debugging hard. When AYON itself is running in console mode, the server
    inherits the AYON console so its output can be seen there. Otherwise the
    console window of the server is hidden and its output is discarded.
    """

    # Should be as last hook because it modifies process launch kwargs
    order = 1000
    app_groups = {"zbrush"}
    platforms = {"windows"}
    launch_types = {LaunchTypes.local}

    def execute(self):
        kwargs = self.launch_context.kwargs or {}
        if is_using_ayon_console():
            # AYON runs in console mode, let the server write to the same
            # console. No creationflags are used on purpose so the console
            # of the parent process is inherited.
            kwargs.update({
                "creationflags": 0,
                "stdout": None,
                "stderr": None,
            })
        else:
            # AYON runs without a console, keep the console window of the
            # server hidden and discard its output.
            kwargs.update({
                "creationflags": subprocess.CREATE_NO_WINDOW,
                "stdout": subprocess.DEVNULL,
                "stderr": subprocess.DEVNULL,
            })
        self.launch_context.kwargs = kwargs
