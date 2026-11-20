"""Open the workfile of the launched AYON context in ZBrush.

ZBrush executes every '*.py' file it finds in the directories listed in
'ZBRUSH_PLUGIN_PATH' when it starts (ZBrush 2026 and newer). The path of
the workfile is passed in 'AYON_ZBRUSH_OPEN_WORKFILE' by the pre-launch
hook of the addon, this plugin only opens it.

Using the ZBrush Python SDK keeps the feature platform independent, no
external ZScript execution and no simulated key presses are needed.
"""
import os
import tempfile

WORKFILE_ENV_KEY = "AYON_ZBRUSH_OPEN_WORKFILE"
LOG_FILENAME = "ayon_zbrush_open_workfile.log"


def _log(message):
    """Write result of the open next to other temporary files.

    The output of the ZBrush Python VM ends up in the ZBrush console,
    a file is easier to look at when the workfile does not open.
    """
    try:
        log_path = os.path.join(tempfile.gettempdir(), LOG_FILENAME)
        with open(log_path, "w") as stream:
            stream.write(message)
    except Exception:  # noqa: BLE001 - logging must never break ZBrush
        pass


def _open_workfile(workfile_path):
    """Open a workfile in ZBrush using the ZBrush Python SDK."""
    import zbrush.commands as zbc

    zbc.set_next_filename(workfile_path)
    zbc.press("File:Open:Open")
    return zbc.get_last_used_filename()


def main():
    workfile_path = os.environ.pop(WORKFILE_ENV_KEY, None)
    if not workfile_path:
        # ZBrush started without AYON asking for a workfile
        return

    try:
        opened_path = _open_workfile(workfile_path)
    except Exception as exc:  # noqa: BLE001 - plugin must not break ZBrush
        _log("Failed to open '{}': {!r}".format(workfile_path, exc))
        return

    _log(
        "Requested workfile: {}\nOpened workfile: {}".format(
            workfile_path, opened_path)
    )


main()
