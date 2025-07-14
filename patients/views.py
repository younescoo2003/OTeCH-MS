from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from utils.renderers import StatusInJSONRenderer
from .models import Patient, PatientMedicine, PatientProgressMonitoring
from .serializers import PatientSerializer, PatientRegisterSerializer, PatientProgressMonitoringSerializer, PatientMedicineSerializer
from drf_yasg.utils import swagger_auto_schema

class PatientProfileView(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [StatusInJSONRenderer]

    @swagger_auto_schema(
        operation_description="Retrieve the authenticated patient's profile",
        responses={200: PatientSerializer, 404: 'Patient not found'}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        # Return the Patient object related to the authenticated user
        return Patient.objects.get(user=self.request.user)


class PatientRegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [StatusInJSONRenderer]

    @swagger_auto_schema(
        operation_description="Register a new patient account",
        request_body=PatientRegisterSerializer,
        responses={
            201: 'Returns access and refresh tokens',
            400: 'Validation errors'
        }
    )
    def post(self, request):
        serializer = PatientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            refresh = RefreshToken.for_user(patient.user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
                },
                status=status.HTTP_201_CREATED
            )

        return Response({'errors': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class PatientProgressMonitoringViewSet(viewsets.ModelViewSet):
    serializer_class = PatientProgressMonitoringSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [StatusInJSONRenderer]

    @swagger_auto_schema(
        operation_description="List all progress monitoring records for the authenticated patient",
        responses={200: PatientProgressMonitoringSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new progress monitoring record for the authenticated patient",
        request_body=PatientProgressMonitoringSerializer,
        responses={201: PatientProgressMonitoringSerializer, 400: 'Validation errors'}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific progress monitoring record",
        responses={200: PatientProgressMonitoringSerializer, 404: 'Record not found'}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing progress monitoring record",
        request_body=PatientProgressMonitoringSerializer,
        responses={200: PatientProgressMonitoringSerializer, 400: 'Validation errors', 404: 'Record not found'}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update an existing progress monitoring record",
        request_body=PatientProgressMonitoringSerializer,
        responses={200: PatientProgressMonitoringSerializer, 400: 'Validation errors', 404: 'Record not found'}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a progress monitoring record",
        responses={204: 'No content', 404: 'Record not found'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        # Patients can only access their own progress monitoring
        return PatientProgressMonitoring.objects.filter(patient__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=Patient.objects.get(user=self.request.user))



class PatientMedicineViewSet(viewsets.ModelViewSet):
    serializer_class = PatientMedicineSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    renderer_classes = [StatusInJSONRenderer]

    @swagger_auto_schema(
        operation_description="List all medications for the authenticated patient",
        responses={200: PatientMedicineSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Add a new medication for the authenticated patient",
        request_body=PatientMedicineSerializer,
        responses={201: PatientMedicineSerializer, 400: 'Validation errors'}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific medication record",
        responses={200: PatientMedicineSerializer, 404: 'Record not found'}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing medication record",
        request_body=PatientMedicineSerializer,
        responses={200: PatientMedicineSerializer, 400: 'Validation errors', 404: 'Record not found'}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update an existing medication record",
        request_body=PatientMedicineSerializer,
        responses={200: PatientMedicineSerializer, 400: 'Validation errors', 404: 'Record not found'}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a medication record",
        responses={204: 'No content', 404: 'Record not found'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        # Patients can only access their own medicines
        return PatientMedicine.objects.filter(patient__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=Patient.objects.get(user=self.request.user))
