"""
Module for testing Web-app functionalities.
"""

import os
import pytest
from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
import app
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# load environment variables
# mongo_uri = os.environ.get("MONGO_URI")
flask_port = os.environ.get("FLASK_RUN_PORT")
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


class Tests:
    """
    Test class for DeepFace functionalities.
    """

    @pytest.fixture
    def test_home_get(self):
        """
        Test the app GET home route at launch
        """
        response = app.test_client().get("/")
        assert response.status_code == 200

    def test_home_post(self):
        """
        Test does the app respond to a given image.
        """
        test_img_path = (
            "web-app\img\man.jpg"
        )
        with open(test_img_path, "rb") as image_file:
            image_data = image_file.read()
        response = app.test_client().post(
            "/",
            data={"image": (image_data, "man.jpg")},
            content_type="multipart/form-data",
        )
        assert response.status_code == 200

    def test_gallery_route(self):
        """
        Test the app GET gallery route at launch
        """
        response = app.test_client().get("/gallery")
        assert response.status_code == 200

    def test_check_status(self):
        """
        Test the whether image id are generated correctly
        """
        sample_id = "sample_id"
        images_collection.insert_one(
            {"_id": sample_id, "processed": False, "emotion": "happy"}
        )
        response = images_collection.find_one({"_id": ObjectId(sample_id)})
        assert response == 200
        images_collection.delete_many({})
