from django.http.response import StreamingHttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ActivityForm, AddParticipantForm
from django.urls import reverse
from defense.models import AddParticipant
from django.contrib.auth.forms import AuthenticationForm, authenticate
from django.contrib.auth import login
from . import Image_Salute
from .camera import VideoCamera
from defense.models import ActivityModels, ActivityReport, AddParticipant
from time import time
# from .forms import UserCreation
  
import logging
import pdb


def index(request):
    return redirect("defense:login")

def auth(request):#, username, password):
   # pdb.set_trace()
    
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
            return redirect('defense:login')
    
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
    if request.method == 'GET':
        context ={"form":form}
        return render(request, 'defense/activity.html', context)
    else:
        form = ActivityForm(request.POST)
        context ={"form":form}
        # form = ActivityForm(instance = a)
        if form.is_valid():
            form.save()
            return redirect("defense:image_render", personnel_id = request.POST.get('id'))
        return render(request, 'defense/activity.html', context)

def add_participant(request):
    # pdb.set_trace()
    if not request.user.is_authenticated:
        return redirect("defense:login")
    if request.method == 'GET':
        context = {'form':AddParticipantForm()}
        items = AddParticipant.objects.all().order_by('-id')[:5]
        context['items'] = items
        return render(request, 'defense/add_participant.html', context)
    else:
        context = {"form":ActivityForm()}
        form = AddParticipantForm(request.POST)
        form.save()

        return redirect("defense:activity")

def generate_report(request, personnel_id):
    if not request.user.is_authenticated:
        return redirect("defense:login")
    details = ActivityModels.objects.get(pk=personnel_id)
    results = ActivityReport()
    ref_participant = AddParticipant.objects.filter(personnel_id=personnel_id).first()
    # ref_participant_activiy = ActivityModels.objects.get(pk=personnel_id)
    results.photo = details.photo
    results.id = ref_participant
    results.name = ref_participant.name
    print(ref_participant)
    # results.id = AddParticipant.objects.get(pk=personnel_id)
    if(details.activity1):
        photo = details.photo.split(',')[1]
        activity1_results = Image_Salute.run(photo)
        results.activity1 = activity1_results[0]
        results.salute_angle = activity1_results[1]
    context = results.__dict__
    print(context.keys())
    results.save()
    return render(request, 'defense/final_report.html',context )


def gen(camera):
    while True:
        img = camera.get_frame()
        yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')

def image_render(request, personnel_id):
    if request.method == "GET":
        return render(request, 'defense/image_render.html')
    else:
        return redirect("defense:add_participant")

def video_capture(request):
    camera = VideoCamera()
    camera.start = time()
    return StreamingHttpResponse(gen(camera), content_type='multipart/x-mixed-replace; boundary=frame')
            

# Create your views here.

