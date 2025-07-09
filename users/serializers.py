from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
import uuid
import re
import random
from datetime import timedelta, datetime
from django.conf import settings
from django.core.cache import caches

auth_cache = caches['auth']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    temp_token = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'password', 'role', 'temp_token')

    def validate(self, data):
        phone_number = data.get('phone_number')
        temp_token = data.get('temp_token')

        cached_token = auth_cache.get(f'verified_{phone_number}')
        if cached_token is None:
            raise serializers.ValidationError('Temp Token has been expired')

        if temp_token != cached_token:
            raise serializers.ValidationError('Invalid Temp Token')


        if len(data['password']) < 8:
            raise serializers.ValidationError("Password is too small")
        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            role=validated_data['role']
        )
        return user

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        if not re.match(r"^\+989\d{9}$", data['phone_number']):
            raise serializers.ValidationError("Invalid phone number")
        
        user = authenticate(phone_number=data.get('phone_number'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError("Invalid phone number or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        data['user'] = user
        return data


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def validate_phone_number(self, value):
        if not re.match(r"^\+989\d{9}$", value):
            raise serializers.ValidationError("Invalid phone number")
        return value

    def validate(self, data):
        c = auth_cache.get(f'verify_{data.get('phone_number')}')
        if c!= None:
            if c['send_time'] + timedelta(seconds=settings.NUMBER_DELAY_SECONDS) > datetime.now():
                raise serializers.ValidationError(f"wait for {(c['send_time']+timedelta(seconds=settings.NUMBER_DELAY_SECONDS)-datetime.now()).seconds} seconds")
        return data

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        otp = random.randint(100000, 999999)
        temp_token = str(uuid.uuid4())
        auth_cache.set(f'verify_{phone_number}', {'otp':otp, 'temp_token': temp_token, 'send_time': datetime.now()}, timeout=300)  # OTP valid for 5 minutes
        print(f"OTP for phone number {phone_number}: {otp}")
        return {'phone_number': phone_number, 'otp': otp, 'temp_token': temp_token}

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    otp = serializers.IntegerField(required=True)
    temp_token = serializers.CharField(required=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')
        temp_token = data.get('temp_token')

        cached_data = auth_cache.get(f'verify_{phone_number}')
        if cached_data is None:
            raise serializers.ValidationError("OTP expired or not found.")
        
        tk = cached_data.get('temp_token', None)
        if tk == None or tk != temp_token:
            raise serializers.ValidationError('Invalid Temp Token')

        if int(otp) != int(cached_data.get('otp', '0')):
            raise serializers.ValidationError("Invalid OTP.")
        return data

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        auth_cache.set(f'verified_{phone_number}', validated_data.get('temp_token'), timeout=30*60) # user can complete register for 30 minutes
        auth_cache.delete(f'verify_{phone_number}')
        return {'phone_number', phone_number}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'role']
