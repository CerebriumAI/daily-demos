from typing import Optional
from pydantic import BaseModel

from daily import *
from pet_detection import PetDetection 

class Item(BaseModel):
    room: str


def predict(item, run_id, logger):
    item = Item(**item)
    
    ##On startup, connect to room
    bot_name = "Pet Detector"

    Daily.init()
    pet_detector = PetDetection()
    client = pet_detector.client

    client.set_user_name(bot_name)
    ##only join if not in call already
    pet_detector.join(item.room)
    for participant in client.participants():
        if participant != "local":
            client.set_video_renderer(participant, callback = pet_detector.on_video_frame)

    try:
        while pet_detector.isRunning():
            pass
    except KeyboardInterrupt:
        client.leave()
        print('\nInterrupted by user')
    
    client.leave()
    return {"message": "Call has finished running"}
