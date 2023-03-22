from django.db import models
from django.contrib.auth.models import User
from core.models import Post


class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=500)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} - {self.content}"



