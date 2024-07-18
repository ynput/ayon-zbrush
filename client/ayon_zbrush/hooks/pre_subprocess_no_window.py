import subprocess
from ayon_applications import PreLaunchHook, LaunchTypes


class LaunchServerNoWindow(PreLaunchHook):
    """Specifically for Zbrush to make the AYON tools launching faster
    """

    # Should be as last hook because must change launch arguments to string
    order = 1000
    app_groups = {"zbrush"}
    platforms = {"windows"}
    launch_types = {LaunchTypes.local}

    def execute(self):

        self.launch_context.kwargs.update({
            "creationflags": subprocess.CREATE_NO_WINDOW,
            "stdout": None,
            "stderr": None
        })
