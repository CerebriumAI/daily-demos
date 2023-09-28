from typing import Optional
from pydantic import BaseModel
from daily import *
from content_moderation import ContentModeration 

class Item(BaseModel):
    # Add your input parameters here
    room: str

def predict(item, run_id, logger):
    item = Item(**item)
    
    ##On startup, connect to room
    bot_name = "Content Moderator"

    Daily.init()
    content_moderator = ContentModeration()
    client = content_moderator.client

    client.set_user_name(bot_name)
    content_moderator.join(item.room)
    for participant in client.participants():
        if participant != "local":
            client.set_video_renderer(participant, callback = content_moderator.on_video_frame)
    
    while content_moderator.isRunning():
        pass

    return {"message": "Call has finished running"} # return your results 

if __name__ == "__main__":
    predict("",  "", "")