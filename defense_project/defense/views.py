from django.shortcuts import render, redirect
from django.contrib.auth import authenticate 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ActivityForm, AddParticipantForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from defense.models import AddParticipant
from . import Image_Salute
# from .forms import UserCreation
  
import logging
import pdb


def auth(request, username, password):
    user = authenticate(username, password)
    if user is None:
        logging.warn("User not created!!")
    else:
        logging.warn("created!")
    return render(request, 'defense/login.html', {'form':user})



# def register(request):
#     # pdb.set_trace()
    
#     if request.method == 'GET':
#         form = UserCreationForm()
#         context = {'form':form }
#         return render(request, 'registration/register.html', context)
#     if request.method == 'POST':
#         pdb.set_trace()
#         form = UserCreationForm(request.POST)
#         context = {'form':form }
#         if form.is_valid():
#             context = {'form':form}
#             form.save()
#             # messages.success(request, "Registered Sucessfully!")    
#             return render(request, "<h1> Sucessfully registrated </h1>")
#         else:
#             return render(request, 'registration/register.html', context)

def register(request):  
    if request.method == 'POST':
          
        form = UserCreationForm(request.POST)  
        if form.is_valid():  
            form.save()  
            messages.success(request, 'Account created successfully')

    else:  
        form = UserCreationForm()  
    return render(request, 'registration/register.html',{'form':form })  

# @login_required(login_url= reverse('defense:login'))
def activity(request):
    form = ActivityForm()
    pdb.set_trace()
    context ={"form":ActivityForm()}
    # pdb.set_trace()
    if request.method == 'GET':
        return render(request, 'defense/activity.html', context)
    else:
        # pdb.set_trace()
        a= {}
        for key, value in request.POST.items():
            if key.startswith('csrf') or key == 'login':
                # logging.warn(request.POST.get(key)[:10])
                continue
            a.update({key: value})
        form = ActivityForm(request.POST)
        # form = ActivityForm(instance = a)
        form.save()
        return render(request, 'defense/activity.html', context)

def add_participant(request):
    # pdb.set_trace()
    if request.method == 'GET':
        context = {'form':AddParticipantForm()}
        items = AddParticipant.objects.all().order_by('-id')[:5]
        context['items'] = items
        return render(request, 'defense/add_participant.html', context)
    else:
        pdb.set_trace()
        context = {"form":ActivityForm()}
        form = AddParticipantForm(request.POST)
        form.save()

        return render(request, 'defense/activity.html', context)


# Create your views here.
