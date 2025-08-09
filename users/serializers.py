from rest_framework import serializers
from .models import User
from utils.validations import validate_uuid


class UserRegistrationSerializer(serializers.ModelSerializer):
    temp_token = serializers.CharField(max_length=100, validators=[validate_uuid], help_text="Temporary token received after OTP verification.")
    phone_number = serializers.CharField(help_text="User's phone number.")
    password = serializers.CharField(write_only=True, help_text="User's password.")
    first_name = serializers.CharField(help_text="User's first name.")
    last_name = serializers.CharField(help_text="User's last name.")
    email = serializers.EmailField(help_text="User's email address.")
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, help_text="User's role.")

    class Meta:
        model = User
        fields = ['phone_number', 'password', 'first_name', 'last_name', 'email', 'temp_token', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        request = self.context.get('request')
        if data.get('role') == 'admin' and (not request.user or not request.user.is_staff):
            raise serializers.ValidationError("Only admins can create other admins.")
        return data

    def create(self, validated_data):
        validated_data.pop('temp_token')
        user = User.objects.create_user(**validated_data)
        return user


class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(help_text="User's phone number.")
    otp = serializers.CharField(max_length=6, help_text="One-time password.")
    temp_token = serializers.CharField(max_length=100, validators=[validate_uuid], help_text="Temporary token received after sending OTP.")


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(help_text="User's phone number.")
    password = serializers.CharField(style={'input_type': 'password'}, help_text="User's password.")


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(help_text="User's phone number.")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'role']

class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    access_expire_seconds = serializers.IntegerField()

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()