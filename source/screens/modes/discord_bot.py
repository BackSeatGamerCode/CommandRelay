import asyncio

import discord

import source.screens.modes.base_mode as base_mode
import source.setting as setting


class DiscordBot(base_mode.BaseMode):
    def __init__(self, *args, **kwargs):
        self.bot: discord.Client = None

        super().__init__(*args, **kwargs)

    def startup(self):
        self.get_additional_settings("discord_bot", [
            setting.Setting("Bot Token", "token")
        ])

        self.bot = discord.Client()

        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return

            if message.content.startswith("!"):
                response = self.process_command(message.content.lstrip("!"), message.author)
                if response is not None:
                    await message.channel.send(response)

    def _relay_commands(self):
        self.bot.run(self.additional_settings["token"])

    def teardown(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.bot.close())
        loop.stop()
