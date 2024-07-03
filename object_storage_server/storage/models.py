from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Object(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    permitted_users = models.ManyToManyField(User, related_name="permitted_objects")
    url = models.URLField(default=None)
    file_format = models.CharField(max_length=10, default=None)
    size = models.IntegerField(default=0)


    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})
