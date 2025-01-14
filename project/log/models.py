from django.db import models

# Create your models here.
class RequestMessage(models.Model):
    username = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username