from django.db import models
import uuid
import os
from django.contrib.auth.models import User

class Meeting(models.Model):
  token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=50)
  datetime = models.DateTimeField()
  member = models.ManyToManyField(User)
  response = models.JSONField(blank=True, null=True)
  
class Attendee(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.JSONField(blank=True, null=True)
