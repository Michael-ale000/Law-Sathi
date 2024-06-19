from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from NewsPortal.models import MoreUserInfo
from django import forms
from django.forms import ModelForm
from .models import LawyerDetails, Address ,LawyerDocuments

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
            'minlength': '2',
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
            'minlength':'5' 
            }) 
        self.fields['password2'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'password2', 
            'id':'password2', 
            'type':'password', 
            'placeholder':'Confirm Password', 
            'maxlength':'22',  
            'minlength':'5' 
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


class AddressForm(forms.ModelForm):
    PROVINCE_CHOICES = [('Koshi','Koshi'),
                        ('Madhesh','Madhesh'),
                        ('Bagmati','Bagmati'),
                        ('Gandaki','Gandaki'),
                        ('Lumbini','Lumbini'),
                        ('Karnali','Karnali'),
                        ('Sudurpaschim','Sudurpaschim'),
                    ]
    province= forms.ChoiceField(choices=PROVINCE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select',
        'required': '',
        'name': 'province',
        'type':'option',
        'id': 'province',
        'placeholder': 'province'}))
    district= forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'required': '',
        'name': 'district',
        'type':'text',
        'id': 'district',
        'placeholder': 'District'}))
    location= forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'required': '',
        'name': 'location',
        'type':'text',
        'id': 'location',
        'placeholder': 'Location'}))
    class Meta:
        model = Address
        fields = ['province', 'district', 'location']

class LawyerDetailsForm(forms.ModelForm):
    experience = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'required': '',
        'name': 'experience',
        'type': 'number',
        'placeholder': 'Experience (in yearrs)'
    }))
    bar_license= forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'required': '',
        'name': 'license-number',
        'type': 'number',
        'placeholder': 'Bar License Number'
    }))
    average_case_completion_days= forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'required': '',
        'name': 'experience',
        'type': 'text',
        'placeholder': 'Average Days For Case Completion'
    }))
    permanent_address= forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'required': '',
        'name': 'permanent_address',
        'type': 'text',
        'placeholder': 'Permanent_address'
    }))
    class Meta:
        model = LawyerDetails
        fields = ['experience', 'bar_license', 'average_case_completion_days', 'permanent_address',]



class LawyerDocumentsForm(forms.ModelForm):
    license_certificate = forms.FileField( widget=forms.ClearableFileInput(attrs={
        'accept': '.pdf,.doc,.docx',
        'required':'',
        'type':'file',
        'id':'experience-certificate'}))
    citizenship_document = forms.FileField( widget=forms.ClearableFileInput(attrs={
        'accept': '.pdf,.doc,.docx',
        'required':'',
        'type':'file',
        'id':'experience-certificate'}))
    personal_photos = forms.FileField( widget=forms.ClearableFileInput(attrs={
        'accept': '.jpg,.jpeg,.png',
         'required':'',
        'type':'file',
        'id':'id-proof'}))
    class Meta:
        model = LawyerDocuments
        fields = ['license_certificate', 'citizenship_document', 'personal_photos']