import logging
from random import randint
import discord
from discord.ext import commands
from errors.errors import ChannelNotFound
from models.Channel import ChannelModel

from services.nick_service import INickService

LOGGER = logging.getLogger('Bot')

class NickExtension(commands.Cog):
    def __init__(self, bot: commands.Bot, service: INickService):
        self.service = service
        self.bot = bot

    @commands.command(name='createNick', help='Pass a channel to create a nick-change channel')
    @commands.has_permissions(administrator=True)
    async def create_nick_change(self, ctx, channel):
        guild = ctx.message.guild
        author_name = ctx.message.author.name
        channel_id = int(channel.strip('<').strip('>').replace('#', ''))
        channel_name = str(self.bot.get_channel(channel_id))
        LOGGER.debug(f'Creating nick-channel #{channel_name} ({channel_id}) in {guild.name} ({guild.id}) by {author_name}')

        channel = ChannelModel(
            channel_id=channel_id,
            channel_name=channel_name,
            guild_id=guild.id,
            guild_name=guild.name,
        )

        await self.service.create_nick_channel(channel)

        title = 'Troque seu Nick! Basta escrevê-lo aqui.\n\nSe tudo der certo, você terá um ✅'
        nick_embed = discord.Embed(colour=0x4D338E)
        nick_embed.set_thumbnail(
            url=f'https://cdn.discordapp.com/icons/{guild.id}/{ctx.message.guild.icon}.png')

        nick_embed.add_field(name='Mudança de Nick', value=f'{title}')
        await self.bot.get_channel(channel_id).send(embed=nick_embed)
        await ctx.send('Nick-change channel sucessfully created.')

    @commands.command(name='deleteNick', help='Pass a nick-change channel to make it a normal channel')
    @commands.has_permissions(administrator=True)
    async def delete_nick_channel(self, ctx, channel):
        guild = ctx.message.guild
        author_name = ctx.message.author.name
        channel_id = int(channel.strip('<').strip('>').replace('#', ''))
        channel_name = str(self.bot.get_channel(channel_id))
        LOGGER.debug(f'Delete nick-channel #{channel_name} ({channel_id}) in {guild.name} ({guild.id}) by {author_name}')

        channel = ChannelModel(
            channel_id=channel_id,
            channel_name=channel_name,
            guild_id=guild.id,
            guild_name=guild.name,
        )

        try:
            await self.service.delete_nick_channel(channel_id, guild.id, channel)

            LOGGER.debug(f'Nick-channel #{channel_name} ({channel_id}) in {guild.name} ({guild.id}) is sucessfully deleted')
            await ctx.send('Sucessfully deleted as a nick-change channel')
        except ChannelNotFound as e:
            await ctx.send('This channel is not a nick-change channel.')
        except:
            await ctx.send('Something going wrong : /')


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.user.id:
            channel = await self.service.find_nick_channel(message.channel.id)
            if not channel is None:
                LOGGER.debug(f'Trying to change nick of {message.author.name} ({message.author.id}) in {message.guild.name} ({message.guild.id}) #{message.channel.name} ({message.channel.id})')
                # Change Nickname
                check = '✅'
                down_check = '❎'
                try:
                    await message.author.edit(nick=message.content)
                    await message.add_reaction(check)
                    LOGGER.debug(f'Nick changed {message.author.name} -> {message.content} ({message.author.id}) sucessfuly')
                except:
                    await message.add_reaction(down_check)
                    LOGGER.debug(f'Nick change failure {message.author.name} -> {message.content} ({message.author.id})')