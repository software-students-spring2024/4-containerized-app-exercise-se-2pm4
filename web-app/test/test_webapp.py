"""TEST"""

import os
from unittest.mock import MagicMock
import pytest
from app import app

# Mocking the database collection
mock_collection = MagicMock()

@pytest.fixture
def test_app_client():
    """
    Create and configure a test client for the app.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_post(test_app_client2, monkeypatch):
    """
    Test the POST request to the home page with a sample image.
    """
    # Mock environment variables
    monkeypatch.setenv("FLASK_RUN_PORT", "5000")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("MONGO_PORT", "27017")
    monkeypatch.setenv("MONGO_DB", "test_db")

    # Mocking insert_one method
    mock_collection.insert_one.return_value.inserted_id = "some_object_id"

    # Read test image data
    test_img_path = os.path.join(os.path.dirname(__file__), "../img/man.jpg")
    with open(test_img_path, "rb") as image_file:
        image_data = image_file.read()

    # Send POST request with test image
    response = test_app_client2.post(
        "/",
        data={"image": (image_data, "man.jpg")},
        content_type="multipart/form-data",
    )

    # Check response
    assert response.status_code == 200
    assert b"Image uploaded successfully" in response.data

def test_gallery_route(test_app_client1, monkeypatch):
    """
    Test the GET request to the gallery page.
    """
    # Mock environment variables
    monkeypatch.setenv("FLASK_RUN_PORT", "5000")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("MONGO_PORT", "27017")
    monkeypatch.setenv("MONGO_DB", "test_db")

    # Mocking find method
    mock_collection.find.return_value = [
        {"_id": "some_object_id", "processed": False, "emotion": "loading..."}
    ]

    # Send GET request to gallery
    response = test_app_client1.get("/gallery")

    # Check response
    assert response.status_code == 200
    assert b"loading..." in response.data
