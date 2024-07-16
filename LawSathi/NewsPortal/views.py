from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import transaction,IntegrityError
import os,requests
from dotenv import load_dotenv
from .form import UserSignUpForm,MoreUserInfoForm
from .models import MoreUserInfo
from django.contrib.auth import authenticate,login
from LawyerRecommendation.models import LawyerDetails
from django.urls import reverse
from django.contrib import messages
# Create your views here.
load_dotenv()

def user_landingpage(request):
    try:
        api_key = os.getenv("Newsportal_api")
        url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey={}'.format(api_key)
        news = requests.get(url).json()

        a = news['articles']
        desc =[]
        title =[]
        img =[]
        url=[]

        for i in range(len(a)):
            f = a[i]
            title.append(f['title'])
            desc.append(f['description'])
            img.append(f['urlToImage'])
            url.append(f['url'])
        mylist = zip(title, desc, img,url)
        # print(title)

        context = {'mylist': mylist}

        return render(request, 'newsportal.html', context)
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")


def usersignup(request):
    try:
        
        if request.method == "POST":
            usersignup_from = UserSignUpForm(request.POST)
            moreinfo_form = MoreUserInfoForm(request.POST)
            if usersignup_from.is_valid() and moreinfo_form.is_valid():
                try:
                    with transaction.atomic():
                        user= usersignup_from.save()
                        moreinfo_data = moreinfo_form.cleaned_data  # Get form data
                        moreinfo, created = MoreUserInfo.objects.get_or_create(user=user, defaults=moreinfo_data)
                        if not created:
                            # Update existing MoreUserInfo object if it already exists
                            for attr, value in moreinfo_data.items():
                                setattr(moreinfo, attr, value)
                            moreinfo.save()
                            messages.success(request, 'Account created successfully.')
                        return redirect('userlogin')
                except IntegrityError:
                    return HttpResponse("Error: Integrity Violation. User might already exist.")
                except Exception as e:
                    return HttpResponse(f"Error Occurred: {e}")
            else:
            # If form is not valid, add form errors to messages
                for field, errors in usersignup_from.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        usersignup_from = UserSignUpForm()
        moreinfo_form = MoreUserInfoForm()
        context = {'usersignup_from':usersignup_from,
        'moreinfo_form':moreinfo_form}
        return render(request,'usersignup.html',context)
        # return HttpResponse("Error Occured")
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")


def userlogin(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                try:
                    is_lawyer = LawyerDetails.objects.get(user=user)
                    messages.error(request, 'You Are Lawyer. Login As A Lawayer')
                    url = reverse('lawyerlogin')
                    return redirect(url)
                except LawyerDetails.DoesNotExist:
                    login(request,user)
                    messages.success(request, 'Login Successful.')
                return redirect(user_landingpage)     
            messages.error(request, 'Invalid Username or Password.')
        return render(request,'userlogin.html')
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")