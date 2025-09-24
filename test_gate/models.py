from django.db import models
from django.conf import settings
import os
from datetime import datetime

def video_upload_path(instance, filename):
    # Videos will be uploaded to MEDIA_ROOT/videos/user_<id>/<year>/<month>/<day>/<filename>
    # user_id = instance.user.id
    current_date = datetime.now()
    return os.path.join(
        'videos',
        # f'user_{user_id}',
        str(current_date.year),
        str(current_date.month),
        str(current_date.day),
        filename
    )

class VideoRecording(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  todo: uncomment later
    video_file = models.FileField(upload_to=video_upload_path)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video by {self.user.username} at {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-recorded_at']
