"""
Module for testing Web-app functionalities.
"""

import os
import pytest
from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
from unittest.mock import patch, MagicMock

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# Initialize MongoDB client and collection
client = MongoClient("mongodb://localhost:27017/")
db = client.get_database("image_emotion_db")
images_collection = db["images"]

class TestWebapp:
    """
    Test class for Web-app functionalities.
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
        test_img_path = os.path.join(os.path.dirname(__file__), "../img/man.jpg")
        with open(test_img_path, "rb") as image_file:
            image_data = image_file.read()

            response = app.test_client().post(
                "/",
                data={"image": (image_data, "man.jpg")},
                content_type="multipart/form-data",
            )

        assert response.status_code == 200

    @patch('app.MongoClient')
    def test_gallery_route(self, mock_client):
        """
        Test the GET request to the gallery page.
        """
        mock_db = MagicMock()
        mock_client.return_value = mock_db
        mock_collection = MagicMock()
        mock_db.get_database.return_value.__getitem__.return_value = mock_collection
        mock_collection.find.return_value = [
            {"_id": "1", "image_ref": "../img/man.jpg", "processed": True, "emotion": "happy"},
        ]

        response = app.test_client().get("/gallery")
        
        assert response.status_code == 200
        assert b"../img/man.jpg" in response.data

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

