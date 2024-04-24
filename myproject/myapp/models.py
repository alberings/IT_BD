from django.db import models

class Event(models.Model):
    type = models.CharField(max_length=50)
    path = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField()
    # user_id = models.IntegerField(null=True, blank=True)  # Assuming user ID is an integer

    def __str__(self):
        return f"{self.type} on {self.path} at {self.timestamp}"
