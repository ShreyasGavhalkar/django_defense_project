from django.shortcuts import render
from django.contrib.auth import authenticate
import logging


def auth(request, username, password):
    user = authenticate(username, password)
    if user is None:
        logging.warn("User not created!!")
    else:
        logging.warn("created!")
    return render(request, 'defense/login.html', {'form':user})

# Create your views here.
