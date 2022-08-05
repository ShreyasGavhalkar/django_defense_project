from django.db import models

class AddParticipant(models.Model):
    personnel_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    photo = models.TextField()
    def __str__(self):
        return self.name+"  (id= "+str(self.personnel_id)+")"


class ActivityModels(models.Model):
    id = models.ForeignKey(AddParticipant, to_field = "personnel_id", db_column="participant_id" ,primary_key=True, on_delete=models.CASCADE)
    activity1 = models.BooleanField()
    activity2 = models.BooleanField()
    activity3 = models.BooleanField()
    activity4 = models.BooleanField() 


# Create your models here.
