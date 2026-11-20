# -*- coding: utf-8 -*-
"""Pre-launch to force zbrush startup script."""
import os
import tempfile

from ayon_zbrush import ZBRUSH_HOST_DIR, get_launch_script_path
from ayon_core.lib import get_ayon_launcher_args
from ayon_applications import PreLaunchHook, LaunchTypes

STARTUP_SCRIPT_PATH = os.path.join(
    ZBRUSH_HOST_DIR, "startup", "startup.txt"
)

# Prepended to the startup script when the last workfile should be opened.
# ZBrush executes only one ZScript passed on the command line, an extra
# 'open workfile' argument is ignored. The command must run in the same
# script as the plugin registration, and it must run before it: the
# startup script hands the UI over to a batch file ('ZBRUSH_PLUGIN_PATH'
# is walked by cmd.exe) and then presses 'CLOSE', after which the
# 'File:Open' dialog is no longer confirmed by the key press and the
# workfile is silently not opened (verified in ZBrush 2026.1.2). Opening
# the workfile first does not block the plugin registration that follows.
OPEN_LAST_WORKFILE_ZSCRIPT = """
// Open the last workfile before the AYON plugins are registered
[If, [FileExists, "{filepath}"],
  [IFreeze,
    [FileNameSetNext, "{filepath}"]
    [IKeyPress, 13, [IPress, File:Open:Open]]]
]
"""


class ZBrushStartupScript(PreLaunchHook):
    """Inject AYON environment to Zbrush.

    Note that this works in combination whit Zbrush startup script that
    is creating the environment variable for the AYON Plugin

    Hook `GlobalHostDataHook` must be executed before this hook.
    """
    app_groups = {"zbrush"}
    order = 11
    launch_types = {LaunchTypes.local}

    def execute(self):
        executable_path = self.launch_context.launch_args.pop(0)
        self.launch_context.env["ZBRUSH_EXE"] = executable_path
        # Pop rest of launch arguments - There should not be other arguments!
        remainders = []
        while self.launch_context.launch_args:
            remainders.append(self.launch_context.launch_args.pop(0))

        new_launch_args = get_ayon_launcher_args(
            "run", get_launch_script_path(), executable_path
        )

        # Append as whole list as these arguments should not be separated
        self.launch_context.launch_args.append(new_launch_args)
        last_workfile = self._get_last_workfile()
        startup_script = self._get_startup_script(last_workfile)
        if last_workfile:
            # ZBrush cannot be asked for the opened document, host resolves
            # the current workfile from the environment.
            self.launch_context.env["AYON_CURRENT_ZPR"] = last_workfile

        self.launch_context.launch_args.append([startup_script])

        if remainders:
            self.log.warning((
                "There are unexpected launch arguments in Zbrush launch. {}"
            ).format(str(remainders)))
            self.launch_context.launch_args.extend(remainders)

    def _get_last_workfile(self):
        """Last workfile that should be opened on start.

        Returns:
            Union[str, None]: Path to the last workfile with forward slashes
                or None if no workfile should be opened.
        """
        if not self.data.get("start_last_workfile"):
            self.log.info("It is set to not start last workfile on start.")
            return None

        last_workfile = self.data.get("last_workfile_path")
        if not last_workfile:
            self.log.warning("Last workfile was not collected.")
            return None

        if not os.path.exists(last_workfile):
            self.log.info(
                "Last workfile does not exist: {}".format(last_workfile))
            return None

        return last_workfile.replace("\\", "/")

    def _get_startup_script(self, last_workfile):
        """Startup script for ZBrush that registers AYON plugins.

        The startup script shipped with the addon is used as is when no
        workfile should be opened. Otherwise a copy with the 'open workfile'
        command prepended is used, so the workfile is opened by the same
        script that registers the AYON plugins, before them.

        Args:
            last_workfile (Union[str, None]): Workfile to be opened on start.

        Returns:
            str: Path to startup script for ZBrush.
        """
        if not last_workfile:
            return STARTUP_SCRIPT_PATH

        with open(STARTUP_SCRIPT_PATH, "r") as stream:
            content = stream.read()

        content = (
            OPEN_LAST_WORKFILE_ZSCRIPT.format(filepath=last_workfile)
            + content
        )

        with tempfile.NamedTemporaryFile(
            mode="w",
            prefix="ayon_zbrush_startup_",
            suffix=".txt",
            delete=False,
        ) as stream:
            stream.write(content)
            script_path = stream.name

        self.log.info(
            "ZBrush will open last workfile: {}".format(last_workfile))
        self.log.debug(
            "ZBrush startup script: {}".format(script_path))

        return script_path
