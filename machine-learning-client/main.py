import os
from pymongo import MongoClient
import schedule
import time

"""Module for face analysis"""
from deepface import DeepFace

MONGO_HOST = os.environ.get("DB_HOST", "mongodb_server")

# Load environment variables for MongoDB connection
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)
MONGO_DB = os.environ.get("MONGO_DB", "image_emotion_db")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
mongo_uri = f"mongodb://{DB_USER}:{DB_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
client = MongoClient(mongo_uri)
# db = client["image_emotion_db"]
db = client.get_database(MONGO_DB)
images_collection = db["images"]


def find_unprocessed_data():

    images_need_processing = images_collection.find({"processed": False})

    for image in images_need_processing:
        face_analysis = DeepFace.analyze(
            img_path=image["image_ref"], enforce_detection=False
        )
        images_collection.update_one(
            {"_id": image["_id"]},
            {
                "$set": {
                    "processed": True,
                    "emotion": face_analysis[0]["dominant_emotion"],
                    # Add the date time now here
                }
            },
        )


schedule.every(30).seconds.do(find_unprocessed_data)
while True:
    schedule.run_pending()
    time.sleep(1)

# finding images


print("Emotion:", face_analysis[0]["dominant_emotion"])
print("Gender:", face_analysis[0]["dominant_gender"])
print("Age:", face_analysis[0]["age"])
print("Race:", face_analysis[0]["dominant_race"])
