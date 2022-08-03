from . import views
from . import forms
from django.urls import path, include

urlpatterns = [
    path('', include("django.contrib.auth.urls"), name='login'),
    path('register/', views.register,  name = 'register'),
    path('activity/', views.activity, name = 'activity'),
    # path("login/", views.auth, name = 'login'),

]