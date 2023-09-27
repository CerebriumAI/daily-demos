from typing import Optional
from pydantic import BaseModel

from daily import *
from faster_whisper import WhisperModel


class Item(BaseModel):
    file_id: str

model_size = "large-v2"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")

def predict(item, run_id, logger):
    item = Item(**item)
    
    segments, info = model.transcribe(f"/persistent-storage/{item.file_id}/audio.mp3", beam_size=5)
    with open(f'/persistent-storage/{run_id}/final_transcription.txt', 'wb') as f:
        for segment in segments:
            f.write("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        f.close()
    
    ##TODO: Send file to webhook endpoint
    return {"message": "finished transcribing file"}