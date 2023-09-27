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
    pet_detector.join(item.room)
    ##TODO:get all participants and set video renderer
    
    while pet_detector.isRunning():
        pass

    return {"message": "Call has finished running"}

if __name__ == "__main__":
    predict("",  "", "")