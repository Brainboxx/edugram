from django.db import models
from django.contrib.auth import get_user_model
from core.models import Profile

User = get_user_model()


# Create your models here.
class Conversation(models.Model):
    messaging_user = models.ForeignKey(Profile, related_name='conversation', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-modified_at',)

    def __str__(self):
        return f'{self.messaging_user}'


class Chat(models.Model):
    conversation = models.ForeignKey(Conversation, default='', related_name='messages', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, default='', related_name='created_messages', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_by}'
