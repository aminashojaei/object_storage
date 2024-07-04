from django.db import models
from django.contrib.auth.models import User
import uuid


class Object(models.Model):
    id = models.CharField(primary_key=True, max_length=20, editable=False)
    file_name = models.CharField(max_length=255, default=None)
    file_format = models.CharField(max_length=20, null=True)
    size = models.PositiveIntegerField(default=1)
    date_and_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    permitted_users = models.ManyToManyField(
        User, related_name="permitted_objects")
    url = models.URLField(null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"{uuid.uuid4()}.{self.file_format}"
        self.url = f"https://webdev.s3.ir-thr-at1.arvanstorage.ir/{self.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name

    def get_date(self):
        return self.date_and_time.date()

    def get_hour(self):
        return self.date_and_time.hour

    def get_minute(self):
        return self.date_and_time.minute
