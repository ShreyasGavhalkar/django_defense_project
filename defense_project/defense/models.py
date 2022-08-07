from django.db import models

class AddParticipant(models.Model):
    personnel_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    photo = models.TextField()
    # sort_id = models.AutoField(default=1)
    def __str__(self):
        return self.name+"  (id= "+str(self.personnel_id)+")"


class ActivityModels(models.Model):
    id = models.ForeignKey(AddParticipant, to_field = "personnel_id", db_column="participant_id" ,primary_key=True, on_delete=models.CASCADE)
    activity1 = models.BooleanField()
    activity2 = models.BooleanField()
    activity3 = models.BooleanField()
    activity4 = models.BooleanField()
    photo = models.TextField(unique=True)

class ActivityReport(models.Model):
    id = models.ForeignKey(AddParticipant, to_field = "personnel_id", db_column="participant_id" ,primary_key=True, on_delete=models.CASCADE)
    photo = models.ForeignKey(ActivityModels, to_field = "photo", db_column="photo", on_delete=models.CASCADE )
    name = models.CharField(max_length=200)
    activity1 = models.CharField(max_length=200, default="NP")
    activity2 = models.CharField(max_length=200, default="NP")
    activity3 = models.CharField(max_length=200, default="NP")
    activity4 = models.CharField(max_length=200, default="NP")
    salute_angle = models.FloatField(default=0)
# Create your models here.
