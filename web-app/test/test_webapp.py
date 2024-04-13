""" Module for testing app.py. """

from app import app
from unittest.mock import patch, MagicMock

# Mocking the database collection
mock_collection = MagicMock()

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

