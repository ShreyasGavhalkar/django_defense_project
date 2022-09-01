
# from . import views
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django import forms
from django.forms import ModelForm
from .models import ActivityModels, AddParticipant

# class UserCreation(UserCreationForm):
#     username = forms.CharField(label="username")
#     password1 = forms.CharField(label="password", widget=forms.PasswordInput)
#     password2= forms.CharField(label="password", widget=forms.PasswordInput)

#     def username_clean(self):
#         username = self.cleaned_data['username']
#         new = User.objects.filter(username=username)
#         if new.count():
#             raise ValidationError("User already exists")

#     def clean_password2(self):  
#         password1 = self.cleaned_data['password1']  
#         password2 = self.cleaned_data['password2']  
  
#         if password1 and password2 and password1 != password2:  
#             raise ValidationError("Password don't match")  
#         return password2 


#     def save(self, commit = True):  
#         user = User.objects.create_user(  
#             self.cleaned_data['username'],  
#             self.cleaned_data['password1']  
#         )
#         return user

class ActivityForm(ModelForm):
    # activity1 = forms.BooleanField()
    # activity2 = forms.BooleanField()
    # activity3 = forms.BooleanField()
    # activity4 = forms.BooleanField() 
    class Meta:
        model = ActivityModels
        fields = ['activity1', 'activity2', 'activity3', 'activity4', 'id']

class AddParticipantForm(ModelForm):
    class Meta:
        model = AddParticipant
        fields = ['personnel_id', 'name']
        # exclude = ['photo']

