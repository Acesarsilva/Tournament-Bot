import logging
from random import randint
import discord
from discord.ext import commands
from errors.errors import ChannelNotFound
from models.Channel import ChannelModel
from services.ticket_service import ITicketService

LOGGER = logging.getLogger('Bot')


class TicketExtension(commands.Cog):
    def __init__(self, bot: commands.Bot, service: ITicketService):
        self.service = service
        self.bot = bot

    @commands.command(name='createTicket', help='Pass a channel to create a ticket channel')
    @commands.has_permissions(administrator=True)
    async def create_ticket(self, ctx, channel):
        guild = ctx.message.guild
        author_name = ctx.message.author.name
        channel_id = int(channel.strip('<').strip('>').replace('#', ''))
        channel_name = str(self.bot.get_channel(channel_id))
        LOGGER.debug(
            f'Creating ticket-channel #{channel_name} ({channel_id}) in {guild.name} ({guild.id}) by {author_name}')

        channel = ChannelModel(
            channel_id=channel_id,
            channel_name=channel_name,
            guild_id=guild.id,
            guild_name=guild.name,
        )

        await self.service.create_ticket_channel(channel)

        # Create new embed with reaction
        ticket_embed = discord.Embed(colour=randint(0, 0xffffff))
        ticket_embed.set_thumbnail(
            url=f'https://cdn.discordapp.com/icons/{guild.id}/{ctx.message.guild.icon}.png')

        title = 'Você pode abrir um Ticket reagindo a esta mensagem!'
        ticket_embed.add_field(name='Suporte', value=f'{title}')
        send_ticket_embed = await self.bot.get_channel(channel_id).send(embed=ticket_embed)

        await send_ticket_embed.add_reaction(u'\U0001F3AB')

    @commands.command(name='deleteTicket', help='Pass a ticket channel to make it a normal channel')
    @commands.has_permissions(administrator=True)
    async def delete_ticket_channel(self, ctx, channel):
        guild = ctx.message.guild
        author_name = ctx.message.author.name
        channel_id = int(channel.strip('<').strip('>').replace('#', ''))
        channel_name = str(self.bot.get_channel(channel_id))
        LOGGER.debug(
            f'Deleting ticket-channel #{channel_name} ({channel_id}) in {guild.name} ({guild.id}) by {author_name}')

        channel = ChannelModel(
            channel_id=channel_id,
            channel_name=channel_name,
            guild_id=guild.id,
            guild_name=guild.name,
        )

        try:
            await self.service.delete_ticket_channel(channel_id, guild.id)

            LOGGER.debug(
                f'Ticket-channel #{channel_name} ({channel_id}) in {guild.name} ({guild.id}) is sucessfully deleted')
            await ctx.send('Sucessfully deleted as a nick-change channel')
        except ChannelNotFound as e:
            await ctx.send('This channel is not a ticket channel.')
        except:
            await ctx.send('Something going wrong : /')

    @commands.command(name='closeTicket', help='Close a open ticket')
    @commands.has_permissions(administrator=True)
    async def close_ticket(self, ctx, mentioned_user):
        mentioned_role = mentioned_user.strip('<@&>')
        LOGGER.debug(
            f'Closing a ticket for user {mentioned_role} in {ctx.guild.name} ({ctx.guild.id}) by {ctx.author.name}')
        get_mentioned_role = [items.name for items in ctx.message.author.guild.roles if f'{items.id}' in
                              f'{mentioned_role}']
        get_role = discord.utils.get(
            ctx.message.author.guild.roles, name=f'{get_mentioned_role[0]}')

        await get_role.delete(reason='Removed by command')
        await ctx.message.channel.delete(reason=None)
        LOGGER.debug(
            f'Ticket for user {mentioned_role} in {ctx.guild.name} ({ctx.guild.id}) sucessfully closed by {ctx.author.name}')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id != self.bot.user.id:
            user_channel_id = payload.channel_id
            channel = await self.service.find_ticket_channel(user_channel_id);
            if channel:
                LOGGER.debug(f'Trying to create a ticket for {payload.member.name} ({payload.member.id}) in ({payload.guild_id})')
                # Get guild and roles
                find_guild = discord.utils.find(
                    lambda guild: guild.id == payload.guild_id, self.bot.guilds)
                guild_roles = discord.utils.get(
                    find_guild.roles, name=f'{payload.member.name}')

                if guild_roles is None:
                    # Create new role
                    permissions = discord.Permissions(
                        send_messages=True, read_messages=True)
                    await find_guild.create_role(name=f'{payload.member.name}', permissions=permissions)

                    # Assign new role
                    new_user_role = discord.utils.get(
                        find_guild.roles, name=f'{payload.member.name}')
                    await payload.member.add_roles(new_user_role, reason=None, atomic=True)

                    # Overwrite role permissions
                    admin_role = discord.utils.get(
                        find_guild.roles, name='🏆 Manager Torneios')

                    overwrites = {
                        find_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        new_user_role: discord.PermissionOverwrite(read_messages=True),
                        admin_role: discord.PermissionOverwrite(
                            read_messages=True)
                    }

                    # Create new channel inside a category
                    category = find_guild.get_channel(
                        payload.channel_id).category
                    create_channel = await find_guild.create_text_channel(
                        u'\U0001F4CB-{}'.format(new_user_role), category=category, overwrites=overwrites)

                    LOGGER.debug(f'Ticket for {payload.member.name} ({payload.member.id}) in ({payload.guild_id}) is sucessfully created')
                    await create_channel.send(
                        f'{new_user_role.mention} Seu ticket foi aberto, informe seu problema e em breve um dos nossos '
                        f'{admin_role.mention} irá responder.')
                else:
                    LOGGER.debug(f'The user {payload.member.name} ({payload.member.id}) already has a open ticket in ({payload.guild_id})')
