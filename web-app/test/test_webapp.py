"""
TEST
"""
import os
from unittest.mock import patch, MagicMock
import tempfile
from app import app
import pytest

# Mocking the database collection
mock_collection = MagicMock()

@pytest.fixture
def test_app_client():
    """Fixture to provide a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()  # Set upload folder to temporary directory
    with app.test_client() as client:
        yield client

@pytest.fixture
def monkey_db():
    """Fixture to mock the MongoDB collection."""
    with patch('app.images_collection', mock_collection):
        yield mock_collection

class Tests:
    """Class for testing web-app."""

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
        """Function testing gallery route."""
        # Mocking find method
        mock_collection.find.return_value = [
            {"_id": "some_object_id", "processed": False, "emotion": "loading..."}
        ]

        with patch("app.images_collection", mock_collection):
            with app.test_client() as client:
                response = client.get("/gallery")
                assert response.status_code == 200
                assert b"loading..." in response.data

    def test_home_post_file_upload(self, test_app_client, monkey_db):
        """
        Test the file upload and database insertion.
        """

        # Mocking insert_one method
        mock_collection.insert_one.return_value.inserted_id = "some_object_id"

        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
            tmp.write(b"some_image_binary_data")
            tmp.flush()

            # Send POST request with the temporary image file
            response = test_app_client.post(
                "/",
                data={"image": (tmp, "test_image.jpg")},
                content_type="multipart/form-data",
            )

            # Check file storage
            assert os.path.exists(f"{app.config['UPLOAD_FOLDER']}/{tmp.name.split('/')[-1]}")

            # Check database insertion
            assert response.status_code == 200
            assert b"Image uploaded successfully" in response.data

