import logging
from databases.nick_repository import INickRepository
from errors.errors import ChannelNotFound
from models.Channel import ChannelModel

LOGGER = logging.getLogger('Bot')


class INickService():
    async def create_nick_channel(self, channel: ChannelModel) -> ChannelModel:
        pass

    async def delete_nick_channel(self, channel_id: int, guild_id: int, channel: ChannelModel) -> ChannelModel:
       pass

    async def find_nick_channel(self, channel_id: int) -> ChannelModel:
        pass


class NickService(INickService):
    def __init__(self, repository: INickRepository) -> None:
        super().__init__()
        self.repository = repository

    async def create_nick_channel(self, channel: ChannelModel) -> ChannelModel:
        LOGGER.debug(
            f'Checking if channel #{channel.channel_name} ({channel.channel_id}) in {channel.guild_name} ({channel.guild_id}) is already a nick-channel')
        check = await self.repository.get_channel_by_id(channel.channel_id)
        if(not check is None):
            return check

        LOGGER.debug(
            f'Creating channel #{channel.channel_name} in {channel.guild_name} as a nick-channel')
        new_channel = await self.repository.create_nick_channel(channel)

        LOGGER.debug(
            f'Create #{channel.channel_name} in {channel.guild_name} sucessfully')
        return new_channel

    async def delete_nick_channel(self, channel_id: int, guild_id: int, channel: ChannelModel) -> ChannelModel:
        LOGGER.debug(
            f'Tryng to delete nick-channel ({channel_id}) in ({guild_id})')
        channel = await self.repository.delete_nick_channel(channel_id, guild_id)
        if(channel is None):
            raise ChannelNotFound

        return channel

    async def find_nick_channel(self, channel_id: int) -> ChannelModel:
        return await self.repository.get_channel_by_id(channel_id)
