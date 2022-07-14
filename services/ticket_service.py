import logging
from databases.ticket_repository import ITicketRepository
from errors.errors import ChannelNotFound
from models.Channel import ChannelModel

LOGGER = logging.getLogger('Bot')

class ITicketService():
    async def create_ticket_channel(self, channel: ChannelModel) -> ChannelModel:
        pass

    async def delete_ticket_channel(self, channel_id: int, guild_id: int) -> ChannelModel:
        pass

    async def find_ticket_channel(self, channel_id: int) -> ChannelModel:
        pass

class TicketService(ITicketService):
    def __init__(self, repository: ITicketRepository) -> None:
        super().__init__()
        self.repository = repository

    async def create_ticket_channel(self, channel: ChannelModel) -> ChannelModel:
        LOGGER.debug(
            f'Checking if channel #{channel.channel_name} ({channel.channel_id}) in {channel.guild_name} ({channel.guild_id}) is already a ticket-channel')
        check = await self.repository.get_channel_by_id(channel.channel_id)
        if(not check is None):
            return check

        LOGGER.debug(
            f'Creating channel #{channel.channel_name} in {channel.guild_name} as a ticket-channel')
        new_channel = await self.repository.create_ticket_channel(channel)

        LOGGER.debug(
            f'Create #{channel.channel_name} in {channel.guild_name} sucessfully')
        return new_channel

    async def delete_ticket_channel(self, channel_id: int, guild_id: int) -> ChannelModel:
        LOGGER.debug(
            f'Tryng to delete ticket-channel ({channel_id}) in ({guild_id})')
        channel = await self.repository.delete_ticket_channel(channel_id, guild_id)
        if(channel is None):
            raise ChannelNotFound

        return channel

    async def find_ticket_channel(self, channel_id: int) -> ChannelModel:
        return await self.repository.get_channel_by_id(channel_id)
