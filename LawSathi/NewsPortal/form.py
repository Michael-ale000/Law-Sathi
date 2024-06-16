from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MoreUserInfo
from django import forms
from django.forms import ModelForm

##UserSignupForm
class UserSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ##widgets to include various html attributes
        self.fields['first_name'].label = 'First Name'
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'first_name',
            'id': 'first_name',
            'type': 'text',
            'placeholder': 'First_Name',
            'maxlength': '30',  # Adjust based on your database field length
            'minlength': '2',
        })

        self.fields['last_name'].label = 'Last Name'
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'last_name',
            'id': 'last_name',
            'type': 'text',
            'placeholder': 'Last_Name',
            'maxlength': '30',  # Adjust based on your database field length
            'minlength': '2',
        })
        self.fields['username'].widget.attrs.update({
            'class':'form-input',
            'required':'', 
            'name':'username', 
            'id':'username', 
            'type':'text', 
            'placeholder':'Username', 
            'maxlength': '16', 
            'minlength': '6',
        })
        self.fields['email'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'email', 
            'id':'email', 
            'type':'email', 
            'placeholder':'Email', 
            }) 
        self.fields['password1'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'password1', 
            'id':'password1', 
            'type':'password', 
            'placeholder':'Password', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
        self.fields['password2'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'password2', 
            'id':'password2', 
            'type':'password', 
            'placeholder':'Confirm Password', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
        
    username = forms.CharField(max_length=20 ,label=False)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']


class MoreUserInfoForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select',
        'required': '',
        'name': 'gender',
        'id': 'gender',
        'placeholder': 'Gender'
    }))

    dob = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-input',
        'name': 'dob',
        'id': 'dob',
        'placeholder': 'DOB(YYYY-MM-DD)'
    }))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'required': '',
        'name': 'phone_number',
        'id': 'phone_number',
        'type': 'text',
        'placeholder': 'Enter your phone number'
    }))
    class Meta:
        model = MoreUserInfo
        fields = ['phone_number','gender','dob']

        