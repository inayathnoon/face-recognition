#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 05:06:24 2024

@author: noon
"""

import face_recognition
import cv2
import numpy as np
import time
import csv
from datetime import datetime

# Initialize or load CSV file for recording recognitions
csv_file = 'recognitions.csv'
try:
    with open(csv_file, 'x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "First Recognition Time", "Last Recognition Time"])
except FileExistsError:
    pass

def update_recognition(name):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    with open(csv_file, 'r+', newline='') as file:
        reader = list(csv.reader(file))
        writer = csv.writer(file)
        for row in reader:
            if name in row:
                row[3] = time_str  # Update last recognition time
                break
        else:  # If the name is not found, add a new entry
            writer.writerow([name, date_str, time_str, time_str])
            file.flush()

video_capture = cv2.VideoCapture(0)

start_time = time.time()

# Load sample pictures and learn how to recognize them
inayath_image = face_recognition.load_image_file("inayath.jpg")
inayath_face_encoding = face_recognition.face_encodings(inayath_image)[0]

test1_image = face_recognition.load_image_file("test1.jpg")  # Changed from ravi.jpg
test1_face_encoding = face_recognition.face_encodings(test1_image)[0]

test2_image = face_recognition.load_image_file("test2.jpg")  # Changed from sumit.jpg
test2_face_encoding = face_recognition.face_encodings(test2_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    inayath_face_encoding,
    test1_face_encoding,
    test2_face_encoding
]
known_face_names = [
    "Inayath",
    "test1",  # Changed from Ravi
    "test2"   # Changed from Sumit
]

# Initialize variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                update_recognition(name)  # Update or add recognition to CSV

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display results and rest of the loop remains unchanged
    # ...

    if cv2.waitKey(1) & 0xFF == ord('q') or (time.time() - start_time) > 300:
        break

video_capture.release()
cv2.destroyAllWindows()
