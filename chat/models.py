from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=150, blank=True, default="Hey there! I'm using EliteChat")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient}: {self.content}"

    class Meta:
        indexes = [
            models.Index(fields=['sender', 'recipient', 'timestamp']),
            models.Index(fields=['recipient', 'sender', 'timestamp']),
        ]