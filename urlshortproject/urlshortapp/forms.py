from django import forms
from django.forms import ModelForm
from .models import Urls
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm






#create UrlsForm
class UrlsForm(ModelForm):

    def clean_userLink(self):
        link = self.cleaned_data["userLink"]
        data = link.split(":")
        
        if "https" in data or "http" in data:
            return link

        else:
            raise forms.ValidationError("Not A Viable Link, Include https or http in your link")
        

    class Meta:
        model = Urls
        fields = ["userLink"]
     


        
class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)




    class Meta:
        model = User
        fields = ("username","email","password1","password2")


        
        
        
        
        
        
       
        

    

            
