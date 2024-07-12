from django.db import models

# Create your models here.
class User (models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    device_urls = models.JSONField(default=dict)

    def __str__(self):
        return self.name