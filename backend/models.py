from django.db import models
import uuid


class Device(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TemperatureReading(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temperature}"


class HumidityReading(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.humidity}"
