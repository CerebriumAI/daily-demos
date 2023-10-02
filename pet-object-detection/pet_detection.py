from daily import *
from ultralytics import YOLO
import cv2
from utils import plot_bboxes
from PIL import Image
import numpy as np
import io
import time
import queue
import threading
import random


##Load in model weights
pet_detection = YOLO("weights.pt")

class PetDetection(EventHandler):
  def __init__(self):
    self.client = CallClient(event_handler = self)
    self.is_running = True
    self.message_sent = False
    self.queue = queue.Queue()

    self.camera = Daily.create_camera_device("my-camera", width = 1280, height = 720, color_format = "RGB")
    self.client.update_inputs({
        "camera": {
            "isEnabled": True,
            "settings": {
            "deviceId": "my-camera"
            }
        },
        "microphone": False
    })

    #Since frames are sent every 30ms, we only want to send one every 1s
    self.frame_cadence = 30
    self.frame_count = 0

  def on_participant_left(self, participant, reason):
    if len(self.client.participant_counts()) <=2: ##count is before the user has left
      self.is_running = False

  def on_participant_joined(self, participant):
    if not participant["info"]['isLocal']:
      self.client.set_video_renderer(participant["id"], callback = self.on_video_frame)

  def on_video_frame(self, participant, frame):
    self.frame_count += 1
    if self.frame_count >= self.frame_cadence:
      self.frame_count = 0
      self.queue.put(frame.buffer)
      worker_thread = threading.Thread(target=self.process_frame, daemon=True)
      worker_thread.start()
    

  def process_frame(self):
    buffer = self.queue.get()
    IMAGE_WIDTH = 1280
    IMAGE_HEIGHT = 720

    image = Image.frombytes('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), buffer)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)

    detections = pet_detection(image)
    if len(detections[0].boxes) > 0:
      plotted_image = plot_bboxes(image, detections[0].boxes, score=False)
      plotted_image = cv2.cvtColor(plotted_image, cv2.COLOR_BGR2RGB)
      is_success, buffer = cv2.imencode(".png", plotted_image)
      image_stream = io.BytesIO(buffer)
      self.camera.write_frame(Image.open(image_stream).tobytes())

    self.queue.task_done()  # Indicate that a formerly enqueued task is complete

  def join(self, url):
     self.client.join(url)

  def isRunning(self):
    return self.is_running