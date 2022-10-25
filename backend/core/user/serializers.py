"""
Serializers for the user API view.
"""

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    def create(self, validated_data: dict):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data: dict):
        """
        Update and return user.
        Override required because we must encrypt password.
        """
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
            # We can call the super() method once we remove the password
        
        if password is not None:
            user.set_password(password)
            user.save()
        
        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs: dict):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        ) # If user is not authenticated -> None
        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")
        
        attrs.update(user=user)
        return attrs