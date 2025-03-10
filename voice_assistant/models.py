from django.db import models
from django.utils import timezone

# Create your models here.

class CallSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"Call {self.session_id} at {self.start_time}"

    class Meta:
        ordering = ['-start_time']

class Conversation(models.Model):
    session = models.ForeignKey(CallSession, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    speaker = models.CharField(max_length=20, default='assistant')  # 'user' or 'assistant'
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.speaker} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']
