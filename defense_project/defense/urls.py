from . import views
from . import forms
from django.urls import path, include
app_name = 'defense'
urlpatterns = [
    path('', include("django.contrib.auth.urls"), name='login'),
    path('register/', views.register,  name = 'register'),
    path('activity/', views.activity, name = 'activity'),
    path('add-participant/', views.add_participant, name = 'add_participant'),
    # path("login/", views.auth, name = 'login'),

]