from django.db import models

# Create your models here.
class User (models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Devices (models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()

    def get_Devices(self):
        devices = Devices.objects.all()
        devices_dict = {device.name: device.url for device in devices}
        return devices_dict

    def add_or_update_devices(self,devices_dict):
        for name, url in devices_dict.items():
            device, created = Devices.objects.update_or_create(
                name=name,
                defaults={'url': url},
            )
            if created:
                print(f"Device {name} created.")
            else:
                print(f"Device {name} updated.")

    def delete_device_by_name(name):
        try:
            device = Devices.objects.get(name=name)
            device.delete()
            return True, f"Device '{name}' deleted successfully."
        except Devices.DoesNotExist:
            return False, f"Device '{name}' does not exist."


class ActiveUser(models.Model):
    hashed_id = models.CharField(max_length=255, unique=True)
    user_id = models.IntegerField(default=int)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.hashed_id