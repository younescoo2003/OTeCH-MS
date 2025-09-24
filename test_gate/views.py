from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .models import VideoRecording
from .serializers import VideoRecordingSerializer
from django.conf import settings
import os
import cv2
from django.shortcuts import render

def index(request):
    return render(request, 'test_gate/index.html')

class VideoRecordingViewSet(viewsets.ModelViewSet):
    queryset = VideoRecording.objects.all()
    serializer_class = VideoRecordingSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny] # todo: delete this after user added to video model

    def create(self, request, *args, **kwargs):
        video_file = request.data.get('video_file')

        if not video_file:
            return Response({"detail": "No video file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the file temporarily to check its duration
        # Ensure the media directory exists
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp_video_' + video_file.name)
        with open(temp_file_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        try:
            cap = cv2.VideoCapture(temp_file_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps
            cap.release()

            if duration > 60:  # 60 seconds = 1 minute
                os.remove(temp_file_path) # Remove temp file
                return Response({"detail": "Video duration exceeds 1 minute."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            os.remove(temp_file_path) # Remove temp file
            return Response({"detail": f"Error processing video file: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        # If duration is valid, proceed with saving the video
        # request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Remove the temporary file after successful processing and saving
        os.remove(temp_file_path)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
