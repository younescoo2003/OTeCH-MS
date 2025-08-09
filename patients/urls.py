from django.urls import path
from .views import PatientRetrieveCreateAPIView, PatientRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', PatientRetrieveCreateAPIView.as_view(), name='patient-retrieve-create'),
    path('<int:pk>/', PatientRetrieveUpdateDestroyAPIView.as_view(), name='patient-retrieve-update-destroy'),
]
