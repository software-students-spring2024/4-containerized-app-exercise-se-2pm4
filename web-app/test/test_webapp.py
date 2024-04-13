"""
Module for testing DeepFace functionalities.
"""

import pytest
from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
import app

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# Initialize MongoDB client and collection
client = MongoClient("mongodb://localhost:27017/")
db = client.get_database("image_emotion_db")
images_collection = db["images"]

class TestDeepFace:
    """
    Test class for DeepFace functionalities.
    """

    @pytest.fixture
    def test_home_get(self):
        """
        Test the GET request to the home page.
        """
        response = app.test_client().get("/")
        assert response.status_code == 200

    def test_home_post(self):
        """
        Test the POST request to the home page with a sample image.
        """
        test_img_path = "path/to/sample/image.jpg"
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
        Test the GET request to the gallery page.
        """
        response = app.test_client().get("/gallery")
        assert response.status_code == 200

    def test_check_status(self):
        """
        Test the whether image id are generated correctly.
        """
        sample_id = "sample_id"
        images_collection.insert_one(
            {"_id": sample_id, "processed": False, "emotion": "happy"}
        )
        response = images_collection.find_one({"_id": ObjectId(sample_id)})
        assert response["_id"] == sample_id
        images_collection.delete_many({})

