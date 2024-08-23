from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import transaction,IntegrityError
import os,requests
from dotenv import load_dotenv
from .form import UserSignUpForm,MoreUserInfoForm,UserUpdateForm,MoreUserInfoUpdateForm
from .models import MoreUserInfo
from django.contrib.auth import authenticate,login,logout
from LawyerRecommendation.models import LawyerDetails
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
load_dotenv()

@login_required
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
                        return redirect('login')
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


def user_login(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_staff:
                    login(request,user)
                    return redirect(reverse('admin:index'))
                try:
                    status_check = LawyerDetails.objects.get(user=user)
                    lawyer_check = LawyerDetails.objects.get(user=user)
                    status = status_check.status
                    is_lawyer = lawyer_check.is_lawyer
                    if is_lawyer:
                        if status == "approved":
                            login(request,user)
                            messages.success(request,'Loged In Successfully')
                            url = reverse('lawyerlanding')
                            return redirect(url)
                        else:
                            messages.error(request,'Form Is Not Accepted. Wait For Conformation Mail.')
                            return render(request,'login.html')
                except LawyerDetails.DoesNotExist:
                    login(request,user)
                    messages.success(request, 'Login Successful.')
                return redirect(user_landingpage)     
            messages.error(request, 'Invalid Username or Password.')
        return render(request,'login.html')
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")
    

@login_required
def logout(request):
    try:
        logout(request)
        # messages.success(request,"Loged Out.")
        return redirect('login')  # Redirect to the home page or any other page
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")

def index(request):
    try:
        return render(request,'index.html')
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")
    
def choose(request):
    try:
        return render(request,'choose.html')
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")

@login_required    
def settings(request):
    try:
        if request.method == "POST":
            user_form = UserUpdateForm(request.POST, instance=request.user)
            more_user_info_form = MoreUserInfoUpdateForm(request.POST, instance=request.user.moreuserinfo)
            if user_form.is_valid() and more_user_info_form.is_valid():
                user_form.save()
                more_user_info_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('settings') 
            else:
            # If form is not valid, add form errors to messages
                for field, errors in UserUpdateForm.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}') 
        
        else:
            user_form = UserUpdateForm(instance=request.user)
            more_user_info_form = MoreUserInfoUpdateForm(instance=request.user.moreuserinfo)

        context = {
        'user_form': user_form,
        'more_user_info_form': more_user_info_form,}
        return render(request,'settings.html',context)
    except Exception as e:
        return HttpResponse(f"Error Occurred:{e}")