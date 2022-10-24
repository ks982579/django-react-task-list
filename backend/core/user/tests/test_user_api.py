"""
Tests for the user API.
"""

from re import Match
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# returns full URL path
CREATE_USER_URL = reverse('user:create-user')
TOKEN_URL = reverse("user:token")

def create_user(**params):
    """Create and return a new user for TESTING purposes."""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""
    def setUp(self):
        """Instantiating APIClient object for use throughout testing."""
        self.client = APIClient()
    
    def test_create_user_success(self):
        """Test creating a user is successful."""
        # create paylaod to pass in
        payload = {
            'email': 'test@example.com',
            'password': 'password+123',
            'name': 'John Doe',
        }
        # Post Data to Endpoint
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Fetch user from database to check values instead of the returned value
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        # We also do not want to return 'password'
        self.assertNotIn('password', res.data)
    
    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""
        # same as previous payload / should we make it class variable?
        payload = {
            'email': 'test@example.com',
            'password': 'password+123',
            'name': 'John Doe',
        }
        # pass dictionary in as kwargs
        create_user(**payload)
        # Now try to create user via endpoint
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short_error(self):
        """Test an error is returned if password is less than 5 characters."""
        payload = {
            'email': 'test@example.com',
            'password': 'abc',
            'name': 'John Doe',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
    
    def test_create_token_for_user(self):
        """Test generate token for valid credentials"""
        user_details = {
            'name': 'Teth Adam',
            'email': 'TA@example.com',
            'password': "TestPassword1234",
        }
        create_user(**user_details)
            # Create new user with details 
        payload = {
            'email': user_details.get("email"),
            'password': user_details.get("password"),
        } # Send to endpoint to generate token :)
        res = self.client.POST(TOKEN_URL, payload)
            # We should get back a token
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)
    
    def test_create_token_bad_email(self):
        """Test for returning errors instead of tokens for incorrect email credentials"""
        user_details = {
            "name": "John Doe",
            "email": "jdoe@example.com",
            "password": "DoesNotMatter123",
        }
        create_user(**user_details)
            # Create User for testing
        payload = {
            "email": "jdoe@gmail.com",
            "password": "DoesNotMatter123",
        } # Incorrect Email Address
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            # We should get a 400 BAD REQUEST
        self.assertNotIn("token", res.data)
            # We should not get back a "token"

    def test_create_token_no_email(self):
        """Test for returning errors instead of tokens for no email provided"""
        user_details = {
            "name": "John Doe",
            "email": "jdoe@example.com",
            "password": "DoesNotMatter123",
        }
        create_user(**user_details)
            # Create User for testing
        payload = {
            "email": "",
            "password": user_details.get("password"),
        } # NO Email Address provided
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            # We should get a 400 BAD REQUEST
        self.assertNotIn("token", res.data)
            # We should not get back a "token"
    
    def test_create_token_bad_password(self):
        """Test for returning errors instead of tokens for incorrect password"""
        user_details = {
            "name": "John Doe",
            "email": "jdoe@example.com",
            "password": "DoesNotMatter123",
        }
        create_user(**user_details)
            # Create User for testing
        payload = {
            "email": user_details.get("email"),
            "password": "Incorrect_Password",
        } # Incorrect password
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            # We should get a 400 BAD REQUEST
        self.assertNotIn("token", res.data)
            # We should not get back a "token"

    def test_create_token_bad_password(self):
        """Test for returning errors instead of tokens for NO password"""
        user_details = {
            "name": "John Doe",
            "email": "jdoe@example.com",
            "password": "DoesNotMatter123",
        }
        create_user(**user_details)
            # Create User for testing
        payload = {
            "email": user_details.get("email"),
            "password": "",
        } # NO password provided
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            # We should get a 400 BAD REQUEST
        self.assertNotIn("token", res.data)
            # We should not get back a "token"