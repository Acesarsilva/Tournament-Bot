import os
import discord
import logging
from dotenv import load_dotenv
from discord.ext import commands
from databases.implementation.mongo_nick_repository import MongoNickRepository
from databases.implementation.mongo_ticket_repository import MongoTicketRepository
from extensions.ticket import TicketExtension

from init_bot import LendasBot
from extensions.nick import NickExtension
from extensions.message import MessageExtension
from services.nick_service import NickService
from services.ticket_service import TicketService
from utils.mongo_connect import mongo_connect

# Logging
LOGGER = logging.getLogger('Bot')
LOGGER_HANDLER = logging.FileHandler(
    filename='./logs/bot.log', encoding='utf-8', mode='w')
# Discord
intents = discord.Intents.default()
intents.members = True
intents.presences = True
BOT = commands.Bot(command_prefix=commands.when_mentioned_or('&'),
                   description='Lendas e-Sports Bot', intents=intents)

DISCORD_TOKEN = 'Your Discord Token'

if __name__ == '__main__':
    # Configure Logging
    LOGGER_HANDLER.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    LOGGER.addHandler(LOGGER_HANDLER)
    LOGGER.setLevel(logging.DEBUG)
    # Starting mongoDB client
    database = mongo_connect(port=27017, database_name='les-bot')
    if(database is None):
         LOGGER.fatal('Mongo connection failed')
         print('Mongo connection failed')
    else:
        # Loading extensions
        BOT.add_cog(LendasBot(BOT))
        BOT.add_cog(MessageExtension(BOT))
        BOT.add_cog(NickExtension(BOT, NickService(MongoNickRepository(database))))
        BOT.add_cog(TicketExtension(BOT,TicketService(MongoTicketRepository(database))))
        LOGGER.info('Bot now is running')
        BOT.run(DISCORD_TOKEN, reconnect=True)
