""" Module for testing app.py. """

from unittest.mock import patch, MagicMock
from io import BytesIO
from app import app
import pytest


# Mocking the database collection
mock_collection = MagicMock()

@pytest.fixture
def test_app_client():
    """Fixture to provide a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def monkey_db():
    """Fixture to mock the MongoDB collection."""
    with patch('app.images_collection', mock_collection):
        yield mock_collection

class Tests:
    '''
    class for testing web-app
    '''
    def test_sanity_check(self):
        """Function sanity check."""
        expected = True
        actual = True
        assert actual == expected, "Expected True to be equal to True!"

    def test_index(self):
        """Function testing index."""
        response = app.test_client().get("/")
        assert response.status_code == 200
    
    def test_gallery_route(self):
        '''
        gallery test
        '''
        # Mocking find method
        mock_collection.find.return_value = [
            {"_id": "some_object_id", "processed": False, "emotion": "loading..."}
        ]

        with patch("app.images_collection", mock_collection):
            with app.test_client() as client:
                response = client.get("/gallery")
                assert response.status_code == 200
                assert b"loading..." in response.data




    def test_home_post(self, test_app_client, monkeypatch):
        """Test the POST request to the home page with simulated image data."""
        monkeypatch.setenv("FLASK_RUN_PORT", "5000")
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("MONGO_PORT", "27017")
        monkeypatch.setenv("MONGO_DB", "test_db")
    
        # Mocking insert_one method
        mock_collection.insert_one.return_value.inserted_id = "some_object_id"
    
        # Simulate image data
        image_data = BytesIO(b"some_image_binary_data")
    
        # Send POST request with simulated image data
        response = test_app_client.post(
        "/",
        data={"image": (image_data, "test_image.jpg")},
        content_type="multipart/form-data",
    )
    
        # Check response
        assert response.status_code == 200
        assert b"Image uploaded successfully" in response.data

