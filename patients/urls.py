from django.urls import path
from .views import PatientProfileView, PatientRegisterView, PatientProgressMonitoringViewSet, PatientMedicineViewSet
from rest_framework.permissions import IsAdminUser

urlpatterns = [
    path('profile/', PatientProfileView.as_view(), name='patient-profile'),
    path('register/', PatientRegisterView.as_view(), name='patient-register'),
    # Patient-facing endpoints
    path('my-progress-monitoring/', PatientProgressMonitoringViewSet.as_view({'get':'list', 'post':'create'}), name='patient-progress-monitoring'),
    path('my-progress-monitoring/<int:pk>/', PatientProgressMonitoringViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete':'destroy'})),
    path('my-medicines/', PatientMedicineViewSet.as_view({'get':'list', 'post':'create'}), name='patient-medicines'),
    path('my-medicines/<int:pk>/', PatientMedicineViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch':'partial_update', 'delete': 'destroy'}), name='patient-medicines-detail'),
]
