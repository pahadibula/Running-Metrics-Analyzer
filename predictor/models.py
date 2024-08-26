from django.db import models

# Create your models here.
# predictor/models.py

from django.db import models
from django.contrib.auth.models import User

class RunningData(models.Model):
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    distance = models.FloatField()  # in kilometers
    minutes = models.IntegerField()  # minutes taken for the run
    seconds = models.IntegerField()  # seconds taken for the run
    pace = models.FloatField()  # pace in minutes per kilometer
    avg_bpm = models.IntegerField()  # average beats per minute
    stride = models.FloatField()  # stride length in meters
    cadence = models.FloatField()  # steps per minute
    date = models.DateTimeField(auto_now_add=True)  # New field


    def __str__(self):
        return f"Distance: {self.distance} km, Pace: {self.pace} min/km"
