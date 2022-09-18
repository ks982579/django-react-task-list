"""
Tests for Models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):
    """Test Models."""
    def test_create_user_with_email_successful(self):
        "Test creating a user with an email successfully/"
        email = "Test@example.com"
        password = "TestPassword+123"
        UserModel = get_user_model()
        user = UserModel.objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@ExAmple.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.CoM', 'test4@example.com'],
        ]
        UserModel = get_user_model()

        for email, expected_value in sample_emails:
            user = UserModel.objects.create_user(email, 'Password+123')
            self.assertEqual(user.email, expected_value)