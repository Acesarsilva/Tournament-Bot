import json
import discord
from random import randint
from discord.ext import commands

#TODO Tournament Menager
class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='t4v4', help='Create a TFT 4v4 Tournament')
    @commands.has_permissions(administrator=True)
    async def t4v4(self, ctx, channel):
        guild_id = ctx.message.guild.id
        channel_id = int(channel.strip('<').strip('>').replace('#', ''))
        title = 'Para fazer sua inscrição basta enviar uma mensagem neste canal com o seu time.'

        with open('./databases/tournament.json', 'r') as file:
            tournament_data = json.load(file)
            new_tournament = str(guild_id)

            if(new_tournament in tournament_data):
                tournament_data[new_tournament][str(channel_id)] = {}
            else:
                tournament_data[new_tournament] = {str(channel_id):{}}

            with open('./databases/tournament.json', 'w') as new_tournament_data:
                    json.dump(tournament_data, new_tournament_data, indent=4)

        ticket_embed = discord.Embed(colour=randint(0, 0xffffff))
        ticket_embed.set_thumbnail(
            url=f'https://cdn.discordapp.com/icons/{guild_id}/{ctx.message.guild.icon}.png')

        ticket_embed.add_field(name='Um Novo Campeonato 4v4 foi Aberto!', value=f'{title}')
        await self.bot.get_channel(channel_id).send(embed=ticket_embed)

    #TODO Start tournament bracket data and print winners
    @commands.command(name='start', help='Start a Tournament')
    @commands.has_permissions(administrator=True)
    async def startTournament(self, ctx, channel):
        channel_id = int(channel.strip('<').strip('>').replace('#', ''))
        guild_id = str(ctx.guild.id)
        with open('./databases/tournament.json', 'r') as file:
            tournament_data = json.load(file)

        return 0

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        if(message.author.id != self.bot.user.id):
            channel_id = str(message.channel.id)
            guild_id = str(message.guild.id)
            with open('./databases/tournament.json', 'r') as file:
                tournament_data = json.load(file)

            if(guild_id in tournament_data.keys()):
                tournaments = tournament_data[guild_id]
                if(channel_id in tournaments.keys()):
                    tournament = tournaments[channel_id]
                    team = self._getTeamFromMessage(message.content)
                    if(team[0] in tournament.keys()):
                        tournament_data[guild_id][channel_id].pop(team[0])
                        with open('./databases/tournament.json', 'w') as deleted_team:
                            json.dump(tournament_data,deleted_team,indent=4)

                        ticket_embed = discord.Embed(colour=randint(0, 0xffffff))
                        ticket_embed.set_thumbnail(
                            url=f'https://cdn.discordapp.com/icons/{guild_id}/{message.guild.icon}.png')

                        ticket_embed.add_field(name='Suporte', value=f'O time {team[0]} foi saiu do torneio.')
                        await self.bot.get_channel(message.channel.id).send(embed=ticket_embed)

    #TODO On Message Update Listener to Update a Team
    @commands.Cog.listener()
    async def on_message_edit(self,before,after):
        if(after.author.id != self.bot.user.id):
            channel_id = str(after.channel.id)
            guild_id = str(after.guild.id)
            with open('./databases/tournament.json', 'r') as file:
                tournament_data = json.load(file)

            if(guild_id in tournament_data.keys()):
                tournaments = tournament_data[guild_id]
                if(channel_id in tournaments.keys()):
                    tournament = tournaments[channel_id]
                    team = self._getTeamFromMessage(after.content)
                    if((len(team) == 5) and (team[0] in tournament.keys())):
                        tournament_data[guild_id][channel_id][team[0]] = team[1:]
                        with open('./databases/tournament.json', 'w') as updated_team:
                            json.dump(tournament_data,updated_team,indent=4)

                        ticket_embed = discord.Embed(colour=randint(0, 0xffffff))
                        ticket_embed.set_thumbnail(
                            url=f'https://cdn.discordapp.com/icons/{guild_id}/{after.guild.icon}.png')

                        ticket_embed.add_field(name='Suporte', value=f'O time {team[0]} foi atualizado com sucesso.')
                        await self.bot.get_channel(after.channel.id).send(embed=ticket_embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.user.id:
            channel_id = str(message.channel.id)
            guild_id = str(message.guild.id)
            registered = False
            with open('./databases/tournament.json', 'r') as file:
                tournament_data = json.load(file)

            if(guild_id in tournament_data.keys()):
                tournaments = tournament_data[guild_id]
                if(channel_id in tournaments.keys()):
                    tournament = tournaments[channel_id]
                    team = self._getTeamFromMessage(message.content)
                    if(len(team) == 5 and not (team[0] in tournament.keys())):
                        tournament_data[guild_id][channel_id][team[0]] = team[1:]
                        with open('./databases/tournament.json', 'w') as new_team:
                            json.dump(tournament_data,new_team,indent=4)
                            registered = True

                    if(registered):
                        await message.add_reaction('✅')
                    else:
                        await message.add_reaction('❎')






    def _getTeamFromMessage(self, message):
        return ['LeS',1,2,3,4]


def setup(bot):
    bot.add_cog(Tournament(bot))