from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import UrlsForm,UserForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Urls
import uuid as id





# Create your views here.

"""
Function that renders the home view.
has a FORM that takes in the users Link and runs some algorithm to shorten it
the new url is shorten with uuid to give it a unique id each.
"""
def index(request):
    
    if request.method == "POST":
        #set form to data gain from UrlsForm
        form = UrlsForm(request.POST)

        #get the tall long submitted in the form
        talllink = request.POST["userLink"]
        
       #use uid to generate four random words
        uid = str(id.uuid4())[:6]

        #check if the user making request is authenticated
        if request.user.is_authenticated:

        #check if data submitted is valid
            if form.is_valid():

            #save data to database model
                obj = form.save(commit=False)

            #get object related to user
                obj.user = request.user;

                #filter the urls model and get those associated with user
                shortlink = Urls.objects.filter(user=request.user)

                #create short LInk
                new_link = "http://127.0.0.1:8000/" + uid

                #add the data to the model
                shortlink.create(user=request.user,uuid=new_link,userLink=talllink)
            #b = Urls(uuid=new_link,userLink=talllink)
            

                #set form back UrlsForm(empty form)
                form = UrlsForm()

           
                #get urls related to the logged in user
                urls = Urls.objects.filter(user = request.user)

                #return dashboard template with urls passed in
                return render(request,'dashboard.html',{"urls":urls})

            #return user to signup page
            return render(request, "index.html", {'form':form})
        else:
            # Redirect back to the same page if the data
            # was invalid
            return HttpResponseRedirect("signup")
            
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
        if request.method == "POST":

            urls = Urls.objects.filter(user = request.user)
        
            return render(request,"dashboard.html",{"urls":urls})
        
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



"""
function thats going to get the shortlink and redirect user to the tall link
"""
def visitLink(request,pk):
    unqiqueLink = "http://127.0.0.1:8000/" + pk

    #get all links the data related to the user
    try:
        shortLink = Urls.objects.filter(user=request.user).get(uuid=unqiqueLink)
    except:
        messages.error(request, "Link isnt in database!")
        return HttpResponseRedirect("/")
    
    #get tall Link associated new_link
    associatedLink = shortLink.userLink
    return redirect(associatedLink)

    #redirect back to tall link
    #return HttpResponseRedirect("/")




