#for voice
import cv2
import numpy as np
import torch
import datetime
import csv
import os
import pygame
from ultralytics import YOLO

# Load YOLO model
model = YOLO("fire_best.pt")

# Initialize pygame mixer
pygame.mixer.init()

# Load the fire alert sound
fire_alert_sound = pygame.mixer.Sound("Fire_alert.mp3")

def fire_detection1(frame, camera_name, room_name):
    # Perform object detection
    results = model(frame)
    result = results[0]

    for box in result.boxes:
        class_id = result.names[box.cls[0].item()]
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        conf = round(box.conf[0].item(), 2)
        print("Object type:", class_id)
        print("Coordinates:", cords)
        print("Probability:", conf)
        print("---")
        if conf > 0.35:
            # Fire detected, take appropriate action
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            date = timestamp.split('_')[0]
            save_folder = os.path.join('detected_fires', date)
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, f"{camera_name}_{timestamp}.jpg")  # Added .jpg file extension
            # Draw bounding box
            xmin, ymin, xmax, ymax = cords
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            
            # Add text label with confidence score
            label = f"{class_id}: {conf}"
            cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
            cv2.imwrite(save_path, frame)
            
            # Logging into CSV file
            with open('detection_logs.csv', 'a', newline='') as csvfile:
                fieldnames = ['Timestamp', 'Camera Name', 'Room Name', 'Video Link','Event Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writerow({'Timestamp': timestamp, 'Camera Name': camera_name, 'Room Name': room_name, 'Video Link': save_path})
                
            # Play the fire alert sound
            fire_alert_sound.play()
            
    return frame