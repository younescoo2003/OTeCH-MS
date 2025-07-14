from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
import uuid
import re
import random
from datetime import timedelta, datetime
from django.conf import settings
from django.core.cache import caches
from utils.validations import phone_regex, validate_uuid

auth_cache = caches['auth']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Account password (min 8 characters)"
    )
    temp_token = serializers.CharField(
        required=True,
        validators=[validate_uuid],
        help_text="Temporary token from OTP verification"
    )
    phone_number = serializers.CharField(
        required=True,
        validators=[phone_regex],
        help_text="Phone number in international format (+989123456789)"
    )
    first_name = serializers.CharField(
        required=True,
        help_text="User's first name"
    )
    last_name = serializers.CharField(
        required=True,
        help_text="User's last name"
    )
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        help_text="User role: patient, doctor, or admin"
    )

    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'password', 'role', 'temp_token')

    def validate(self, data):
        """
        Validate temporary token and phone number verification status.
        Checks if the temporary token matches the one stored in cache for the phone number.
        """
        phone_number = data.get('phone_number')
        temp_token = data.get('temp_token')

        # Retrieve cached token for the phone number
        cached_token = auth_cache.get(f'verified_{phone_number}')
        if cached_token is None:
            raise serializers.ValidationError('Verification token has expired')
            
        if temp_token != cached_token:
            raise serializers.ValidationError('Invalid verification token')

        return data

    def validate_password(self, value):
        """Validate password length (minimum 8 characters)"""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        return value
        

    def create(self, validated_data):
        """Create a new user with the validated data"""
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role']
        )
        return user

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        validators=[phone_regex],
        help_text="Registered phone number in international format"
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Account password"
    )

    def validate(self, data):
        """Authenticate user with phone number and password"""
        user = authenticate(
            phone_number=data.get('phone_number'),
            password=data.get('password')
        )
        if not user:
            raise serializers.ValidationError("Invalid phone number or password")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        data['user'] = user
        return data


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        validators=[phone_regex],
        help_text="Phone number to send OTP to (international format)"
    )

    def validate(self, data):
        """Validate if OTP can be sent (respecting rate limits)"""
        phone_number = data.get('phone_number')
        cached_data = auth_cache.get(f'verify_{phone_number}')
        
        # Check if we need to wait before sending another OTP
        if cached_data:
            next_send_time = cached_data['send_time'] + timedelta(seconds=settings.NUMBER_DELAY_SECONDS)
            if next_send_time > datetime.now():
                wait_seconds = (next_send_time - datetime.now()).seconds
                raise serializers.ValidationError(f"Please wait {wait_seconds} seconds before requesting another OTP")
                
        return data

    def create(self, validated_data):
        """Generate and store OTP, then return temporary token"""
        phone_number = validated_data['phone_number']
        otp = random.randint(100000, 999999)
        temp_token = str(uuid.uuid4())
        
        # Store OTP and temp token in cache (valid for 5 minutes)
        auth_cache.set(f'verify_{phone_number}', {
            'otp': otp,
            'temp_token': temp_token,
            'send_time': datetime.now()
        }, timeout=300)
        
        # In production, this would send via SMS - here we log for debugging
        print(f"OTP for {phone_number}: {otp}")
        
        return {
            'phone_number': phone_number,
            'otp': otp,
            'temp_token': temp_token
        }

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        validators=[phone_regex],
        help_text="Phone number that received the OTP"
    )
    otp = serializers.IntegerField(
        required=True,
        help_text="6-digit OTP code"
    )
    temp_token = serializers.CharField(
        required=True,
        validators=[validate_uuid],
        help_text="Temporary token from OTP request"
    )

    def validate(self, data):
        """Validate OTP and temporary token against cached values"""
        phone_number = data.get('phone_number')
        otp = data.get('otp')
        temp_token = data.get('temp_token')

        # Retrieve cached OTP data
        cached_data = auth_cache.get(f'verify_{phone_number}')
        if cached_data is None:
            raise serializers.ValidationError("OTP expired or not found")
        
        # Validate temporary token
        cached_token = cached_data.get('temp_token')
        if cached_token is None or cached_token != temp_token:
            raise serializers.ValidationError('Invalid temporary token')
            
        # Validate OTP
        if int(otp) != int(cached_data.get('otp', 0)):
            raise serializers.ValidationError("Invalid OTP")
            
        return data

    def create(self, validated_data):
        """Store verification token after successful OTP validation"""
        phone_number = validated_data['phone_number']
        temp_token = validated_data['temp_token']
        
        # Store verification token for 30 minutes
        auth_cache.set(f'verified_{phone_number}', temp_token, timeout=30*60)
        
        # Clear OTP data from cache
        auth_cache.delete(f'verify_{phone_number}')
        
        return {'phone_number': phone_number}


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        help_text="User's first name"
    )
    last_name = serializers.CharField(
        help_text="User's last name"
    )
    phone_number = serializers.CharField(
        help_text="User's phone number"
    )
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        help_text="User role: patient, doctor, or admin"
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'role']
