from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import RegisterSerializer, LoginSerializer, SendOTPSerializer, VerifyOTPSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'user': {
#                     'phone_number': user.phone_number,
#                     'first_name': user.first_name,
#                     'last_name': user.last_name,
#                 },
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'status':status.HTTP_201_CREATED})
#         return Response({'errors':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {
                    'phone_number': user.phone_number,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'status':status.HTTP_200_OK})
        return Response({'errors':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response({'message': 'OTP sent successfully', 'temp_token': data['temp_token'], 'status':status.HTTP_200_OK})
        return Response({'errors': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response({
                'msg': 'go register',
                'status': status.HTTP_200_OK
            })
        return Response({'errors': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
