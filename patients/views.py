from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer, PatientListSerializer


class PatientRetrieveCreateAPIView(mixins.RetrieveModelMixin,
                                   mixins.CreateModelMixin,
                                   generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PatientListSerializer
        return PatientSerializer

    def get_object(self):
        try:
            return Patient.objects.get(user=self.request.user)
        except Patient.DoesNotExist:
            raise ValidationError({"detail": "The patient record hasn't been created yet."})

    @swagger_auto_schema(
        operation_description="Retrieve the patient record for the logged-in user.",
        responses={
            200: PatientListSerializer(),
            404: "The patient record hasn't been created yet."
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a patient record for the logged-in user.",
        request_body=PatientSerializer,
        responses={
            201: PatientSerializer(),
            400: "Bad Request",
            409: "This user already has a patient profile."
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            self.request.user.is_registration_complete = True
            self.request.user.save()
            serializer.save(user=self.request.user, last_modified_by=self.request.user)
        except IntegrityError:
            raise ValidationError(
                {"detail": "This user already has a patient profile."}
            )

class PatientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(last_modified_by=self.request.user)

    @swagger_auto_schema(
        operation_description="Retrieve the patient record for the logged-in user.",
        responses={
            200: PatientSerializer(),
            404: "Not Found"
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update the patient record for the logged-in user.",
        request_body=PatientSerializer,
        responses={
            200: PatientSerializer(),
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update the patient record for the logged-in user.",
        request_body=PatientSerializer,
        responses={
            200: PatientSerializer(),
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete the patient record for the logged-in user.",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
