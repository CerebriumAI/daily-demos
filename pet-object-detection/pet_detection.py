from daily import *
from ultralytics import YOLO
import cv2
from utils import plot_bboxes
from PIL import Image
import numpy as np

##Load in model weights
pet_detection = YOLO("weights.pt")

class PetDetection(EventHandler):
  def __init__(self):
    self.client = CallClient(event_handler = self)
    self.is_running = True
    self.message_sent = False

  def on_participant_joined(self, participant):
    if not participant["info"]['isLocal']:
      self.client.set_video_renderer(participant["id"], callback = self.on_video_frame)


  def on_video_frame(self, participant, frame):
    IMAGE_WIDTH = frame.width
    IMAGE_HEIGHT = frame.height
    
    image = Image.frombytes('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), frame.buffer)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    detections = pet_detection(image)
    if len(detections[0].boxes) > 0:
      ##TODO: Do something with detection
      if not self.message_sent:
        print('sending')
        self.client.send_app_message("Everyone Relax, but we have a pet in the call👀", None)
        self.message_sent = True

  def join(self, url):
     self.client.join(url)

  def on_call_state_updated(self,state):
    if state == 'left':
      self.is_running = False

  def isRunning(self):
    return self.is_running