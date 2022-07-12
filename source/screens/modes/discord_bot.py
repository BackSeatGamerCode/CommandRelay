import TwitchPyRC
import discord
import asyncio
from signal import SIGINT, SIGTERM

import source.exceptions as exceptions
import source.screens.modes.base_mode as base_mode
import source.setting as setting


class DiscordBot(base_mode.BaseMode):
    def __init__(self, *args, **kwargs):
        self.bot = discord.Client()

        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return

            if message.content.startswith("!"):
                response = self.process_command(message.content.lstrip("!"), message.author)
                if response is not None:
                    await message.channel.send(response)

        super().__init__(*args, **kwargs)

    def startup(self):
        self.get_additional_settings("discord_bot", [
            setting.Setting("Bot Token", "token")
        ])

    def _relay_commands(self):
        self.bot.run(self.additional_settings["token"])

    def teardown(self):
        # self.bot.loop.close()
        for signal in [SIGINT, SIGTERM]:
            self.bot.loop.add_signal_handler(signal, lambda x: x)

        self.bot.loop.close()
