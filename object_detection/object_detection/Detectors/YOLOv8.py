import cv2
from ultralytics import YOLO
import os
import time

from ..DetectorBase import DetectorBase


class YOLOv8(DetectorBase):
  def __init__(self, conf_threshold = 0.7):
    
    super().__init__()
    
    self.conf_threshold = conf_threshold

  def build_model(self, model_dir_path, weight_file_name) :

    try :
      model_path = os.path.join(model_dir_path, weight_file_name)
      self.model = YOLO(model_path)
    
    except :
      raise Exception("Error loading given model from path: {}. Maybe the file doesn't exist?".format(model_path))
  

  def load_classes(self, model_dir_path):

    self.class_list = []

    with open(model_dir_path + "/classes.txt", "r") as f:
        self.class_list = [cname.strip() for cname in f.readlines()]

    return self.class_list


  def get_predictions(self, cv_image):

    if cv_image is None:
      # TODO: show warning message (different color, maybe)
      return None,None
    
    else :     
      self.frame = cv_image   

      class_id = []
      confidence = []
      boxes = []
      result = self.model.predict(self.frame, conf = self.conf_threshold) # Perform object detection on image
      row = result[0].boxes

      for box in row:
        class_id.append(box.cls.numpy().tolist())
        confidence.append(box.conf.numpy().tolist())
        boxes.append(box.xyxy.numpy().tolist())
        
      self.create_predictions_list(class_id,confidence,boxes)
      

      return self.predictions
  