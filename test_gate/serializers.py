from rest_framework import serializers
from .models import VideoRecording

class VideoRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoRecording
        fields = ['id', 'video_file', 'recorded_at']
        read_only_fields = ['id', 'recorded_at']