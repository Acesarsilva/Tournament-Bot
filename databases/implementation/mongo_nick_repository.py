from pymongo.collection import Collection
from databases.nick_repository import INickRepository
from models.Channel import ChannelModel


class MongoNickRepository(INickRepository):
    def __init__(self, database) -> None:
        self.collection: Collection = database['nick']

    async def create_nick_channel(self, channel: ChannelModel) -> ChannelModel:
        return self.collection.insert_one(channel.dict())

    async def delete_nick_channel(self, channel_id: int, guild_id: int) -> ChannelModel:
        return self.collection.find_one_and_delete({"channel_id": channel_id, "guild_id": guild_id})

    async def get_channel_by_id(self, channel_id: int) -> ChannelModel:
        return self.collection.find_one({"channel_id": channel_id})