import TwitchPyRC

import source.exceptions as exceptions
import source.screens.modes.base_mode as base_mode
import source.setting as setting


class TwitchIRCMode(base_mode.BaseMode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot: TwitchPyRC.TwitchIRC = None

    def on_message(self, message: str, username: str, _, tags):
        username = username if tags.display_name is None else tags.display_name

        if message.startswith("!"):
            response = self.process_command(message.lstrip("!"), username)
            if response is not None:
                self.bot.send_message(response)

    def startup(self):
        self.get_additional_settings("twitch_irc", [
            setting.Setting("IRC Token", "token", default="oauth:"),
            setting.Setting("Channel", "channels"),
            setting.Setting("Nickname", "nickname", default="BSGCommandRelayBot"),
            setting.Setting("Server", "server", default="irc.chat.twitch.tv"),
            setting.Setting("Port", "port", cast=int, default=6667),
        ])

        self.bot = TwitchPyRC.TwitchIRC(**self.additional_settings)

        self.bot.on_message = self.on_message

    def _relay_commands(self):
        self.bot.start()

    def teardown(self):
        self.bot.stop()
