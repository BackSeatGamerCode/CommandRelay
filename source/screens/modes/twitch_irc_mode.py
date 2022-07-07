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
        # self.receive_reward("Up", "cpsuperstore")
        # self.receive_reward("Up", "cpsuperstore")
        print(self.additional_settings)

    def _relay_commands(self):
        while self._running:
            print("RELAY")
            time.sleep(3)

    def teardown(self):
        print('bye')
