from django.db import models
from django.utils import timezone

# Create your models here.
class SensorData(models.Model):
    node = models.IntegerField(default=1)
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Node: {self.node}, Temp: {self.temperature}, Humidity: {self.humidity}, Time: {self.timestamp}"
