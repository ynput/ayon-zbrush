from ayon_server.settings import BaseSettingsModel, SettingsField

from .create import CreatePluginsModel


class ZbrushSettings(BaseSettingsModel):
    stop_timer_on_application_exit: bool = SettingsField(
        title="Stop timer on application exit")
    create: CreatePluginsModel = SettingsField(
        default_factory=CreatePluginsModel,
        title="Create plugins"
    )


DEFAULT_VALUES = {
    "stop_timer_on_application_exit": False
}
