"""
Module for testing DeepFace functionalities.
"""

import pytest
from deepface import DeepFace


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
