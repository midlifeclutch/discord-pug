from collections import OrderedDict
import logging
from logging.config import fileConfig
import pprint
import os

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

class Client(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), case_insensitive=True,
            description='A bot to run pugs.', help_command=commands.DefaultHelpCommand(verify_checks=False),
            intents=intents,
        )

        fileConfig('logging.conf')
        self.logger = logging.getLogger(f'pug.{__name__}')

        self.token = os.getenv('DISCORD_TOKEN')
        self.queue_status = False
        self.queue = OrderedDict()
        self.ready = []

    async def setup_hook(self):
        await self.load_extension('bot.cogs.commands')

    async def on_ready(self):
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Activity(type=discord.ActivityType.playing,
                                                             name='Counter-Strike 2'))

        self.logger.info(f'{self.user} connected.')

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            self.logger.info(f'Ignoring command in #{ctx.channel}')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Command is on cooldown ({error.retry_after:.0f}s).')
        else:
            raise error


    def run(self):
        super().run(self.token, reconnect=True)
