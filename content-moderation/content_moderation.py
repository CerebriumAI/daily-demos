from daily import *
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

##Image moderation
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


class ContentModeration(EventHandler):
  def __init__(self):
    self.client = CallClient(event_handler = self)
    self.is_running = True
    self.classes = [
        "drugs", 
        "nudity", 
        "women naked",
        "men naked",
        "weapons",
        "violence"
    ]

  def on_participant_joined(self, participant):
    if not participant["info"]['isLocal']:
      self.client.set_video_renderer(participant["id"], callback = self.on_video_frame)


  def on_video_frame(self, participant, frame):
    
    image = Image.frombytes('RGB', (frame.width, frame.height), frame.buffer)
    inputs = processor(text=self.classes, images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1).tolist()    

    tolerance = 0.7
    if any(abs(x - 0.7) <= tolerance for sublist in probs for x in sublist):
        ##TODO: Do something
        return

  def join(self, url):
     self.client.join(url)

  def on_call_state_updated(self,state):
    if state == 'left':
      self.is_running = False

  def isRunning(self):
    return self.is_running