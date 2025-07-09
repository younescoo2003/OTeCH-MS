from django.core.cache import caches
from rest_framework import serializers
from .models import Patient
from users.serializers import RegisterSerializer, UserSerializer

auth_cache = caches['auth']

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['user', 'national_id', 'birthdate', 'gender', 'marital_status', 'ms_type']
        depth = 0


class PatientRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    temp_token = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = Patient
        fields = ['national_id', 'birthdate', 'gender', 'marital_status', 'ms_type', 'first_name', 'last_name', 'password', 'temp_token', 'phone_number']

    def validate(self, data):
        reg = RegisterSerializer(data=data)
        if reg.is_valid():
            cached_token = auth_cache.get(f'verified_{data['phone_number']}')   

            if cached_token is None:
                raise serializers.ValidationError('Number is Not Verified')
            
            if cached_token != data['temp_token'] or not data['temp_token']:
                raise serializers.ValidationError('Invalid temp token')
        else:
            raise serializers.ValidationError(reg.errors)


        return data

    def create(self, validated_data):
        validated_data['role'] = 'patient'
        reg = RegisterSerializer(data=validated_data)
        user = reg.create(validated_data)

        patient = Patient.objects.create(
            user=user,
            national_id=validated_data['national_id'],
            birthdate=validated_data['birthdate'],
            gender=validated_data['gender'],
            marital_status=validated_data['marital_status'],
            ms_type=validated_data['ms_type'],
        )

        auth_cache.delete(f'verified_{validated_data['phone_number']}')

        return patient
