from models.Channel import ChannelModel


class ITicketRepository:
    def create_ticket_channel(self, channel: ChannelModel) -> ChannelModel:
        pass

    def delete_ticket_channel(self, channel_id: str, guild_id: str) -> ChannelModel:
        pass

    def get_channel_by_id(self, channel_id: str) -> ChannelModel:
        pass