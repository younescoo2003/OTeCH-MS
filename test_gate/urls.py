from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoRecordingViewSet, index

router = DefaultRouter()
router.register(r'video-recordings', VideoRecordingViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('upload/', include(router.urls)),
]