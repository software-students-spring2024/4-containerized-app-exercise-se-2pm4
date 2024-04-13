"""
This module contains the main functionality for the machine learning client.
"""

import os
import time
import schedule
from pymongo import MongoClient
from deepface import DeepFace

MONGO_HOST = os.environ.get("DB_HOST", "mongodb_server")

# Load environment variables for MongoDB connection
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)
MONGO_DB = os.environ.get("MONGO_DB", "image_emotion_db")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
mongo_uri = f"mongodb://{DB_USER}:{DB_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
client = MongoClient(mongo_uri)
db = client.get_database(MONGO_DB)
images_collection = db["images"]


def get_dominant_emotion(path):
    """This function is used to get the dominant emotion"""
    if not path:
        return "No path"
    if not os.path.exists(path):
        return "Invalid path"
    data = DeepFace.analyze(img_path=path, enforce_detection=False)
    return data[0]["dominant_emotion"]


def find_unprocessed_data():
    """This function is used to process unprocessed images to include emotion attribute"""
    images_need_processing = images_collection.find({"processed": False})

    for image in images_need_processing:
        dominant_emotion = get_dominant_emotion(image["image_ref"])
        images_collection.update_one(
            {"_id": image["_id"]},
            {
                "$set": {
                    "processed": True,
                    "emotion": dominant_emotion,
                    # Add the date time now here
                }
            },
        )


def main():
    """Main function"""
    schedule.every(30).seconds.do(find_unprocessed_data)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
