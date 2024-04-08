"""Module for face analysis"""

from deepface import DeepFace

face_analysis = DeepFace.analyze(img_path="./img/man.jpg")
print("Gender:", face_analysis[0]["dominant_gender"])
print("Age:", face_analysis[0]["age"])
print("Race:", face_analysis[0]["dominant_race"])
print("Emotion:", face_analysis[0]["dominant_emotion"])
