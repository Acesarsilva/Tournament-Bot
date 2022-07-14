from json import load
import logging
from discord.ext import commands

from errors.errors import ChannelNotFound

LOGGER = logging.getLogger('Bot')

class LendasBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Discord logged in as {self.bot.user} ({self.bot.user.id})')
        LOGGER.info(f'Discord logged in as {self.bot.user} ({self.bot.user.id})')

    @commands.Cog.listener()
    async def on_resumed(self):
        LOGGER.warning('Bot has reconnected')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Unknown command
        if isinstance(error, commands.CommandNotFound):
            LOGGER.debug(
                f'CommandNotFound in {ctx.message.guild.name} ({ctx.message.guild.id}) by {ctx.message.author.name} ({ctx.message.author.id}) - {error}')
            return await ctx.send(error)

        # Bot does not have permission
        elif isinstance(error, commands.MissingPermissions):
            LOGGER.warning(
                f'MissingPermissions in {ctx.message.guild.name} by {ctx.message.author.name} with {ctx.command.name} - {error}')
            return await ctx.send(error)

        elif isinstance(error, commands.MissingRequiredArgument):
            LOGGER.debug(f'MissingRequiredArgument in {ctx.message.guild.name} by {ctx.message.author.name} with {ctx.command.name} command - {error}')
            if(ctx.command.name == 'createNick'):
                return await ctx.send('Please, pass a channel to create a nick-change channel : )')
            elif(ctx.command.name == 'deleteNick'):
                return await ctx.send('Please, pass a nick-change channel to make it a normal channel : )')
            else:
                return await ctx.send(error)
        # Unexpected Error
        else:
            LOGGER.error(
                f'Unexpected error in guild {ctx.message.guild.name} by {ctx.message.author.name} - {error}')
