# -*- coding: utf-8 -*-
"""Pre-launch hook passing the workfile to open to the AYON host."""
import os

from ayon_applications import PreLaunchHook, LaunchTypes


class ZbrushLastWorkfile(PreLaunchHook):
    """Pass the workfile that should be opened to the launched ZBrush.

    ZBrush executes only one ZScript passed on the command line and that
    is needed for the AYON plugins, so the workfile cannot be a launch
    argument. It is passed in the environment instead and opened by the
    'ayon_workfile' Python plugin of the addon, which ZBrush executes on
    start. This works on all platforms ZBrush 2026 runs on.

    Hook `GlobalHostDataHook` must be executed before this hook.
    """
    app_groups = {"zbrush"}
    order = 12
    launch_types = {LaunchTypes.local}

    def execute(self):
        workfile_path = self._get_workfile()
        if not workfile_path:
            return

        self.launch_context.env["AYON_ZBRUSH_OPEN_WORKFILE"] = workfile_path
        # ZBrush cannot be asked for the opened document, the host resolves
        # the current workfile from the environment.
        self.launch_context.env["AYON_CURRENT_ZPR"] = workfile_path

    def _get_workfile(self):
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
