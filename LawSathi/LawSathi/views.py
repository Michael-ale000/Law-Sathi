from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate,login,update_session_auth_hash
from django.contrib.auth.decorators import login_required


#Creating our views

def landingpage(request):
    return render(request,'landingpage.html')
