import json
import discord
from random import randint
from discord.ext import commands


class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Tournament(bot))