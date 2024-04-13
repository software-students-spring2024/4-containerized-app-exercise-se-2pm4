"""
Module for testing DeepFace functionalities.
"""

import pytest
from deepface import DeepFace
import mlc_deepface


class Tests:
    """
    Test class for DeepFace functionalities.
    """

    @pytest.fixture
    def test_img_path(self):
        """
        Fixture to return the path of the test image within the test class.
        """
        return "./img/man.jpg"

    @pytest.fixture
    def test_invalid_img_path(self):
        """
        Fixture to return the path of the invalid path test image within the test class.
        """
        return "./img/duck.jpg"

    def test_sanity_check(self):
        """
        Test to ensure that the testing framework is functioning correctly.
        """
        expected = True
        actual = True
        assert expected == actual, "Expected True to be equal to True."

    def test_face_attributes(self, test_img_path):
        """
        Test to analyze facial attributes and assert their types.
        """
        face_analysis = DeepFace.analyze(test_img_path)
        face_data = face_analysis[0]
        gender = face_data["dominant_gender"]
        age = face_data["age"]
        race = face_data["dominant_race"]
        emotion = face_data["dominant_emotion"]
        print(gender, age, race, emotion)
        assert isinstance(gender, str)
        assert isinstance(age, int)
        assert isinstance(race, str)
        assert isinstance(emotion, str)

    def test_analyze(self, test_img_path):
        """
        Test to analyze facial attributes and check for specific attributes in the result.
        """
        result = DeepFace.analyze(
            test_img_path, actions=["age", "gender", "race", "emotion"]
        )[0]
        assert "age" in result
        assert "gender" in result
        assert "race" in result
        assert "emotion" in result

    def test_no_path(self):
        """
        Test case where no path is given.
        """
        dominant_emotion = mlc_deepface.get_dominant_emotion("")
        assert dominant_emotion == "No path"

    def test_invalid_path(self, test_invalid_img_path):
        """
        Test case where invalid path is given.
        """
        dominant_emotion = mlc_deepface.get_dominant_emotion(test_invalid_img_path)
        assert dominant_emotion == "Invalid path"

    def test_get_dominant_emotion_with_valid_path(self, test_img_path):
        """
        Test case where valid path is given.
        """
        dominant_emotion = mlc_deepface.get_dominant_emotion(test_img_path)
        assert dominant_emotion == "neutral"
