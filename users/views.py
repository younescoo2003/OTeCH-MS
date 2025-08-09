from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.core.cache import caches
from django.shortcuts import reverse
from django.conf import settings
from .serializers import UserRegistrationSerializer, OTPSerializer, LoginSerializer, PhoneNumberSerializer, TokenRefreshSerializer, MessageSerializer
from .models import User
import random
import uuid
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SendOTPView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_description="Send OTP to user's phone number.",
        request_body=PhoneNumberSerializer,
        responses={
            200: openapi.Response(
                description="OTP sent successfully.",
                examples={
                    "application/json": {
                        "message": "OTP sent successfully.",
                        "temp_token": "a-temporary-token",
                        "next_url": "/api/users/verify-otp/"
                    }
                }
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = str(random.randint(100000, 999999))
            print(f"OTP for {phone_number}: {otp}")  # Print OTP to terminal
            auth_cache = caches['auth']
            temp_token = str(uuid.uuid4())
            auth_cache.set(phone_number, {'otp': otp, 'temp_token':temp_token, 'tries':0}, timeout=600)
            return Response({"message": "OTP sent successfully.", 'temp_token': temp_token, 'next_url': reverse('verify-otp')}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_description="Verify OTP.",
        request_body=OTPSerializer,
        responses={
            200: openapi.Response(
                description="OTP verified successfully.",
                examples={
                    "application/json": {
                        "message": "OTP verified successfully.",
                        "next_url": "/api/users/register/"
                    }
                }
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            phone_number = serializer.validated_data['phone_number']
            auth_cache = caches['auth']
            cached_data = auth_cache.get(phone_number)
            if not cached_data:
                return Response({"message": "OTP is expired", 'code':'otp_expired'}, status=status.HTTP_400_BAD_REQUEST)

            if cached_data['temp_token'] != serializer.validated_data['temp_token']:
                return Response({'message':'Invalid temp token', 'code':'invalid_tomp_token'}, status=status.HTTP_400_BAD_REQUEST)

            if cached_data['tries'] > settings.VERIFY_OTP_MAX_TRIES:
                return Response({'message':'Too many tries.', 'code':'too_many_tries'}, status=status.HTTP_400_BAD_REQUEST)

            if cached_data['otp'] == otp:
                auth_cache.set(phone_number, {'otp': otp, 'verified': True, 'temp_token': cached_data['temp_token']}, timeout=600)
                return Response({"message": "OTP verified successfully.", 'next_url': reverse('register')}, status=status.HTTP_200_OK)
            else:
                auth_cache.set(phone_number, {'otp': otp, 'temp_token': cached_data['temp_token'], 'tries':cached_data['tries']+1}, timeout=600)
                return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user.",
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully.",
                schema=TokenRefreshSerializer
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            auth_cache = caches['auth']
            cached_data = auth_cache.get(phone_number)
            if not cached_data:
                return Response({"message": "OTP verification is expired", 'code':'otp_expired'}, status=status.HTTP_400_BAD_REQUEST)
                
            if cached_data['temp_token'] != serializer.validated_data['temp_token']:
                return Response({'message':'Invalid temp token', 'code':'invalid_tomp_token'}, status=status.HTTP_400_BAD_REQUEST)

            if cached_data.get('verified', False):
                user = serializer.save()
                auth_cache.delete(phone_number)
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "User registered successfully.",
                    'refresh':str(refresh),
                    'access':str(refresh.access_token),
                    'access_expire_seconds': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds
                }, status=status.HTTP_201_CREATED)

            return Response({"message": "Phone number not verified.", 'code':'phone_number_not_verified'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_description="Login a user.",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="User logged in successfully.",
                schema=TokenRefreshSerializer
            ),
            401: "Invalid credentials"
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'access_expire_seconds': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds
                })
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)