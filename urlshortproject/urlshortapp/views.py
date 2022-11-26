from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import UrlsForm,UserForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Urls
import uuid 




# Create your views here.
def index(request):
    
    if request.method == "POST":
        #set form to data gain from UrlsForm
        form = UrlsForm(request.POST)
       
        uid = str(uuid.uuid4())[:6]

        #check if data is valid
        if form.is_valid():

            #save data to database model
            obj = form.save(commit=False)
            obj.user = request.user;
            obj.save()
            form = UrlsForm()

           

            if request.user.is_authenticated:
                urls = Urls.objects.filter(user = request.user)
                return render(request,'dashboard.html',{"urls":urls})

            #return user to signup page
            
            return HttpResponseRedirect('signup')
        else:
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "index.html", {'form':form})
    else:
        #if get method
        #show the home page with form
        form = UrlsForm
        return render(request,"index.html",{"form":form})


"""
function to display the sign up page to the user
"""
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('login')
        else:
            return render(request, "signup.html", {"form": form})
            
    form = UserForm
    return render(request, "signup.html", {"form": form})



"""
function to display login html and log valid users in.

"""
def Login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"Login Successful")
                return HttpResponseRedirect('dashboard')
            else:
                return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})
    
    form = AuthenticationForm()
    return render(request, "login.html",{"form":form})



def dashboard(request):
    if request.user.is_authenticated:

        urls = Urls.objects.filter(user = request.user)
        
        return render(request,"dashboard.html",{"urls":urls})
    else:
        messages.success(request,"Login First Please")
        return HttpResponseRedirect("login")

@login_required
def Logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return HttpResponseRedirect("/")




