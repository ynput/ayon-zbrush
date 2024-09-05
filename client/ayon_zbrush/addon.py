# -*- coding: utf-8 -*-
import os
from ayon_core.addon import click_wrap, AYONAddon, IHostAddon

from .version import __version__

ZBRUSH_HOST_DIR = os.path.dirname(os.path.abspath(__file__))


def get_launch_script_path():
    return os.path.join(
        ZBRUSH_HOST_DIR,
        "api",
        "launch_script.py"
    )


class ZbrushAddon(AYONAddon, IHostAddon):
    name = "zbrush"
    version = __version__
    host_name = "zbrush"

    def add_implementation_envs(self, env, _app):
        # Add AYON zscripts
        new_zbrush_paths = [
            os.path.join(ZBRUSH_HOST_DIR, "api", "zscripts")
        ]
        old_zbrush_path = env.get("ZBRUSH_PLUGIN_PATH") or ""
        for path in old_zbrush_path.split(os.pathsep):
            if not path:
                continue
            norm_path = os.path.normpath(path)
            if norm_path not in new_zbrush_paths:
                new_zbrush_paths.append(norm_path)
        env["ZBRUSH_PLUGIN_PATH"] = os.pathsep.join(new_zbrush_paths)

        # Set some applications defaults
        defaults = {
            "AYON_LOG_NO_COLORS": "True",
            "WEBSOCKET_URL": "ws://localhost:6001"
        }
        for key, value in defaults.items():
            if not env.get(key):
                env[key] = value
        # Remove auto screen scale factor for Qt
        env.pop("QT_AUTO_SCREEN_SCALE_FACTOR", None)

    def cli(self, click_group):
        click_group.add_command(cli_main.to_click_obj())

    def get_workfile_extensions(self):
        return [".zpr"]

    def get_launch_hook_paths(self, app):
        if app.host_name != self.host_name:
            return []
        return [
            os.path.join(ZBRUSH_HOST_DIR, "hooks")
        ]


@click_wrap.group(ZbrushAddon.name, help="Zbrush related shell commands.")
def cli_main():
    pass


@cli_main.command(help="Call AYON plugins command")
@click_wrap.option("--launcher", help="Type of Launcher")
def run_with_zscript(launcher):
    from ._run_zscript import main

    main(launcher)
