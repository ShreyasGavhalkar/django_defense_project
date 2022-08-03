from django.shortcuts import render
from django.contrib.auth import authenticate 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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


# Create your views here.
