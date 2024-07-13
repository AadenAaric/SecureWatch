from django.db import models

# Create your models here.
class User (models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    device_urls = models.JSONField(default=dict)

    def __str__(self):
        return self.name
    

class ActiveUser(models.Model):
    hashed_id = models.CharField(max_length=255, unique=True)
    user_id = models.IntegerField(default=int)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.hashed_id