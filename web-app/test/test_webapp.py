"""
TEST
"""

from unittest.mock import patch, MagicMock
import tempfile
import pytest
from app import app


# Mocking the database collection
# pylint: disable=W0621
# pylint: disable=W0613
mock_collection = MagicMock()


@pytest.fixture(scope="module")
def test_client():
    """
    test client
    """
    flask_app = app
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture
def monkey_db():
    """Fixture to mock the MongoDB collection."""
    with patch("app.images_collection", mock_collection):
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

    def test_home_post_file_upload(self, test_client, monkey_db):
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
            response = test_client.post(
                "/",
                data={"image": (tmp, "test_image.jpg")},
                content_type="multipart/form-data",
            )
            # Check database insertion
            assert response.status_code == 200
            assert b"Image uploaded successfully" in response.data
