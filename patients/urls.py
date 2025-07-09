from django.urls import path
from .views import PatientProfileView, PatientRegisterView

urlpatterns = [
    path('profile/', PatientProfileView.as_view(), name='patient-profile'),
    path('register/', PatientRegisterView.as_view(), name='patient-register')
]
