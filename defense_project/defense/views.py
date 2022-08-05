from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ActivityForm, AddParticipantForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from defense.models import AddParticipant
from django.contrib.auth.forms import AuthenticationForm, authenticate
from django.contrib.auth import login
from . import Image_Salute
# from .forms import UserCreation
  
import logging
import pdb


def auth(request):#, username, password):
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('defense:add_participant')
            else:
                return messages.warning("User not found!")

        else:
            return messages.warning(request, "Invalid Form!")
    
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})



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
    
    if not request.user.is_authenticated:
        return redirect("defense:login")
    form = ActivityForm()
    # pdb.set_trace()
    context ={"form":ActivityForm()}
    # pdb.set_trace()
    if request.method == 'GET':
        return render(request, 'defense/activity.html', context)
    else:
        # pdb.set_trace()
        form = ActivityForm(request.POST)
        # form = ActivityForm(instance = a)
        form.save()
        return redirect("defense:generate_report", personnel_id = request.POST.get('id'))

def add_participant(request):
    # pdb.set_trace()
    if not request.user.is_authenticated:
        return redirect("defense:login")
    # pdb.set_trace()
    if request.method == 'GET':
        context = {'form':AddParticipantForm()}
        items = AddParticipant.objects.all().order_by('-id')[:5]
        context['items'] = items
        return render(request, 'defense/add_participant.html', context)
    else:
        # pdb.set_trace()
        context = {"form":ActivityForm()}
        form = AddParticipantForm(request.POST)
        form.save()

        return redirect("defense:activity")

def generate_report(request, personnel_id):
    if not request.user.is_authenticated:
        return redirect("defense:login")
    Output = "at report gen page with id "+str(personnel_id)
    return HttpResponse(Output)


# Create your views here.
