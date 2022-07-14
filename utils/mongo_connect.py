import logging
import pymongo

LOGGER = logging.getLogger('Bot')

mongoUrl = 'Your Mongo URL'

def mongo_connect(port: int, database_name: str):
    try:
        client = pymongo.MongoClient(mongoUrl, serverSelectionTimeoutMS=5000)
        LOGGER.info(f'MongoClient connected sucessfuly')
        LOGGER.info(client.server_info())
        return client[database_name]
    except:
        LOGGER.fatal('Mongo connection failed')