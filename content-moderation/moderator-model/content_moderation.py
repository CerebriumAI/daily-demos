from daily import *
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import queue
import threading

##Image moderation
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

class ContentModeration(EventHandler):
  def __init__(self):
    self.client = CallClient(event_handler = self)
    self.is_running = True
    self.queue = queue.Queue()
    self.classes = [
        "drugs", 
        "nudity", 
        "women naked",
        "men naked",
        "weapons",
        "violence"
    ]
    #Since frames are sent every 30ms, we only want to send one every 1s
    self.frame_cadence = 60
    self.frame_count = 0
    self.thread_count = 0

  def on_participant_joined(self, participant):
    if not participant["info"]['isLocal']:
      self.client.set_video_renderer(participant["id"], callback = self.on_video_frame)

  def on_video_frame(self, participant, frame):
      self.frame_count += 1
      if self.frame_count >= self.frame_cadence and self.thread_count < 5:
        self.frame_count = 0
        self.thread_count += 1
        self.queue.put({"buffer":frame.buffer, "participant": participant, "width": frame.width, "height": frame.height})
        worker_thread = threading.Thread(target=self.process_frame, daemon=True)
        worker_thread.start()

  def process_frame(self):
    item = self.queue.get()
    
    image = Image.frombytes('RGB', (item["width"], item["height"]), item["buffer"])
    inputs = processor(text=self.classes, images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1).tolist()    

    tolerance = 0.7
    matching_indexes = [(i, j) for i, sublist in enumerate(probs) for j, x in enumerate(sublist) if abs(x - tolerance) <= tolerance]
    if len(matching_indexes) > 0:
        matching_classes = [self.classes[j] for i, j in matching_indexes]
        matching_classes = ", ".join(matching_classes)
        self.client.send_app_message({'participant': item["participant"], 'message': f"Their is a content violation for {matching_classes}"})

    self.queue.task_done()  # Indicate that a formerly enqueued task is complete
    self.thread_count -= 1
    return

  def join(self, url):
     self.client.join(url)

  def on_participant_left(self, participant, reason):
    if len(self.client.participant_counts()) <=2: ##count is before the user has left
      self.is_running = False

  def isRunning(self):
    return self.is_running