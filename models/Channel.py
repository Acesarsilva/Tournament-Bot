from datetime import datetime
from pydantic import BaseModel

class ChannelModel(BaseModel):
    channel_id: int
    channel_name: str
    guild_id: int
    guild_name: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()