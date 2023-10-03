from typing import Optional
from pydantic import BaseModel
from pydub import AudioSegment
from daily import *
import time
import requests
import json
import os

class Item(BaseModel):
    # Add your input parameters here
    room: str

def predict(item, run_id, logger):
    item = Item(**item)
    
    ##On startup, connect to room
    bot_name = "Meeting Transcriber"

    Daily.init()
    client = CallClient()
    client.set_user_name(bot_name)
    client.join(item.room)
    speaker = Daily.create_speaker_device("my-speaker", sample_rate = 16000, channels = 1)
    Daily.select_speaker_device("my-speaker")
    
    if not os.path.exists(f"/persistent-storage/{run_id}"):
        os.makedirs(f'{run_id}')
    
    with open(f'/persistent-storage/{run_id}/output.raw', 'wb') as f:
        while True:
            if client.participant_counts()['present'] == 1:
                client.leave()
                f.close()
                break
            buffer = speaker.read_frames(160)
            f.write(buffer)
            time.sleep(0.01)
    
    wav_audio = AudioSegment.from_raw(f'/persistent-storage/{run_id}/output.raw', format="raw", 
                                  frame_rate=16000, 
                                  channels=1, 
                                  sample_width=2)
    wav_audio.export(f'/persistent-storage/{run_id}/final.wav', format='wav')
    client.leave()

    ##send instructions to model to transcribe meeting
    url = "http://your-cerebrium-whisper-url.com"
    headers = {
        "Authorization": "JWT Token",
        "Content-Type": "application/json"
    }
    data = {
        "file_id": run_id,
        "webhook_endpoint": "Any Webhook endpoint to return transcription to"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    logger.info(response.status)

    return {"message": "Call has finished running - busy transcribing"} 