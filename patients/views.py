from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer, PatientRegisterSerializer, PatientProgressMonitoringSerializer, PatientMedicineSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class PatientProfileView(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the Patient object related to the authenticated user
        return Patient.objects.get(user=self.request.user)


class PatientRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PatientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            refresh = RefreshToken.for_user(patient.user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'status':status.HTTP_201_CREATED})

        return Response({'errors':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})


class PatientProgressMonitoringViewSet(viewsets.ModelViewSet):
    serializer_class = PatientProgressMonitoringSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Patients can only access their own progress monitoring
        return PatientProgressMonitoring.objects.filter(patient__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=Patient.objects.get(user=self.request.user))


class PatientMedicineViewSet(viewsets.ModelViewSet):
    serializer_class = PatientMedicineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Patients can only access their own medicines
        return PatientMedicine.objects.filter(patient__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=Patient.objects.get(user=self.request.user))
