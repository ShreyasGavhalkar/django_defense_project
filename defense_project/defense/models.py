from django.db import models

class ActivityModels(models.Model):
    activity1 = models.BooleanField()
    activity2 = models.BooleanField()
    activity3 = models.BooleanField()
    activity4 = models.BooleanField() 


class AddParticipant(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    photo = models.TextField()
# Create your models here.
