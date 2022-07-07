import time

import source.screens.modes.base_mode as base_mode
import source.setting as setting


class TwitchIRCMode(base_mode.BaseMode):
    def startup(self):
        self.get_additional_settings("twitch_irc", [
            setting.Setting("IRC Token", "token", default="oauth:"),
            setting.Setting("Channel", "channel"),
            setting.Setting("Nickname", "nickname", default="BSGCommandRelayBot"),
            setting.Setting("Server", "server", default="irc.chat.twitch.tv"),
            setting.Setting("Port", "port", cast=int, default=6667),
        ])


    def _relay_commands(self):
        print(self.additional_settings)
        while self._running:
            print("RELAY")
            time.sleep(3)
