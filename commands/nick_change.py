import json
import discord
from random import randint
from discord.ext import commands

class NickChange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='nick', help='Create a nick change channel')
    @commands.has_permissions(administrator=True)
    async def createnickchange(self, ctx, channel):
        guild_id = ctx.message.guild.id
        channel_id = int(channel.strip('<').strip('>').replace('#', ''))
        title = 'Basta escrever seu Nick seguindo o modelo fixado!'

        with open('./databases/nick_change.json', 'r') as file:
            nick_data = json.load(file)
            new_nick = str(guild_id)

            # Update existing nick channel
            if new_nick in nick_data:
                nick_data[new_nick] += [channel_id]
                with open('./databases/nick_change.json', 'w') as update_nick_data:
                    json.dump(nick_data, update_nick_data, indent=4)

            # Add new nick channel
            else:
                nick_data[new_nick] = [channel_id]
                with open('./databases/nick_change.json', 'w') as new_nick_data:
                    json.dump(nick_data, new_nick_data, indent=4)

        # Create new embed
        nick_embed = discord.Embed(colour=randint(0, 0xffffff))
        nick_embed.set_thumbnail(
            url=f'https://cdn.discordapp.com/icons/{guild_id}/{ctx.message.guild.icon}.png')

        nick_embed.add_field(name='Nick Change', value=f'{title}')
        await self.bot.get_channel(channel_id).send(embed=nick_embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.user.id:
            with open('./databases/nick_change.json', 'r') as file:
                nick_data = json.load(file)
        
            channel_id = list(nick_data.values())
            user_channel_id = message.channel.id
        
            for itens in channel_id:
                if user_channel_id in itens:
                    # Change Nickname
                    check = '✅'
                    down_check = '❎'
                    try:
                        await message.author.edit(nick=message.content)
                        await message.add_reaction(check)
                    except:
                        await message.add_reaction(down_check)


def setup(bot):
    bot.add_cog(NickChange(bot))