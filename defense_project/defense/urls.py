from . import views
from . import forms
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from 

app_name = 'defense'
urlpatterns = [
    path('', views.index, name = "index"),
    path('login/', views.auth, name='login'),
    path('auth/', views.auth, name = "auth"),
    path('register/', views.register,  name = 'register'),
    path('activity/', views.activity, name = 'activity'),
    path('add-participant/', views.add_participant, name = 'add_participant'),
    path('report/<int:personnel_id>', views.generate_report, name = "generate_report"),
    path('image_render/<int:personnel_id>', views.image_render, name="image_render"),
    path('video_capture', views.video_capture, name = "video_capture"),
    # path("login/", views.auth, name = 'login'),
]