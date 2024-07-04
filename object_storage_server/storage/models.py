from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid



class Object(models.Model):
    
    id = models.CharField(primary_key=True, max_length=10, editable=False)
    file_name = models.CharField(max_length=255, default=None)
    size = models.PositiveIntegerField(default=1)
    # date_and_time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, default=None)  # Example values: 'mp3', 'mp4', etc.
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"{uuid.uuid4()}.{self.type}"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
