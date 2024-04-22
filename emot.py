import time
from flask import session
import keras
import cv2
from keras.models import model_from_json
from keras.preprocessing import image
import keras.utils as image
# from keras .preprocessing import image
# from keras.preprocessing.image import ImageDataGenerator

import numpy as np


import face_recognition
import pickle
from datetime import datetime
from core import rec_face_image
from database import *
# Load pre-trained model for emotion detection
model = model_from_json(open(r"model\facial_expression_model_structure.json", "r").read())
model.load_weights(r'model\facial_expression_model_weights.h5')

# Load Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(r'model\haarcascade_frontalface_default.xml')

# Define emotion labels
emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')


def detect_emotion(path, id1):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    emotion_interval = 30
    time_counter = 0
    frame_number = 0

    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to capture image")
            break
        frame_number += 1
        time_counter += 1 / fps

        if time_counter >= emotion_interval:
            detect_emotion(path)
            time_counter = 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_number + (fps * emotion_interval)))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            detected_face = img[y:y+h, x:x+w]
            detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY)
            detected_face = cv2.resize(detected_face, (48, 48))
            img_pixels = image.img_to_array(detected_face)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255

            predictions = model.predict(img_pixels)
            max_index = np.argmax(predictions[0])
            emotion = emotions[max_index]
            print("************************",detected_face)

            FaceFileName = "static/test.jpg" #Saving the current image from the webcam for testing.
        

            cv2.imwrite(FaceFileName, detected_face)
            names = rec_face_image(FaceFileName)
            print("!!!!!!!!!!!!!!!!!!!!",names)

            

            # if emotion == 'happy':
            #     q1 = "INSERT INTO emotiondetection VALUES(NULL, '%s', '%s', 5, curdate())" % (id1, emotion)
            # elif emotion == 'neutral':
            #     q1 = "INSERT INTO emotiondetection VALUES(NULL, '%s', '%s', 4, curdate())" % (id1, emotion)
            # elif emotion == 'angry':
            #     q1 = "INSERT INTO emotiondetection VALUES(NULL, '%s', '%s', 2, curdate())" % (id1, emotion)
            # else:
            #     q1 = "INSERT INTO emotiondetection VALUES(NULL, '%s', '%s', 1, curdate())" % (id1, emotion)
            # res1 = insert(q1)
            # time.sleep(5)
            for name in names:
                q = "SELECT * FROM user WHERE user_id='%s'" % name
                res = select(q)
                print("^^^^^^^^^^^^^^^^^^",res)
                
                if res:
                    
                    session['aid'] = id1
                    session['stid'] = name
                    if emotion == 'happy':
                        q1 = "INSERT INTO emotiondetection VALUES(NULL, '%s', '%s', 5, curdate(),'1')" % (name, emotion)
                    elif emotion == 'neutral':
                        q1 = "INSERT INTO emotiondetection VALUES(NULL, '%s', '%s', 4, curdate(),'1')" % (name, emotion)
                    elif emotion == 'angry':
                        q1 = "INSERT INTO emotiondetection VALUES(NULL, '%s', '%s', 2, curdate(),'1')" % (name, emotion)
                    else:
                        q1 = "INSERT INTO emotiondetection VALUES(NULL, '%s', '%s', 1, curdate(),'1')" % (name, emotion)
                    res1 = insert(q1)

        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    


import cv2
import numpy as np
import face_recognition
import pickle

def rec_face_image(imagepath):
    data = pickle.loads(open('faces.pickles', "rb").read())

    image = cv2.imread(imagepath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb, model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.4)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            if len(counts) == 1:
                name = max(counts, key=counts.get)
            else:
                name = "-1"

        if name != "Unknown":
            names.append(name)

    return names