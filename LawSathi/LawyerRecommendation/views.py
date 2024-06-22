from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .form import UserSignUpForm,MoreUserInfoForm,AddressForm,LawyerDetailsForm,LawyerDocumentsForm
from django.db import transaction,IntegrityError
from NewsPortal.models import MoreUserInfo
from django.contrib.auth.models import User
from .models import Address,LawyerDetails,LawyerDocuments
from datetime import date
from django.contrib.auth import authenticate,login


# Create your views here.
def serialize_date(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def deserialize_date(date_str):
    return date.fromisoformat(date_str)


def lawyersignup1(request):
     try:
        if request.method =="POST":
            user_form = UserSignUpForm(request.POST ,prefix='form1')
            moreinfo_form= MoreUserInfoForm(request.POST, prefix='form2')  
            if user_form.is_valid() and moreinfo_form.is_valid():
                moreinfo_form = moreinfo_form.cleaned_data
                if 'dob' in moreinfo_form:
                    moreinfo_form['dob'] = serialize_date(moreinfo_form['dob'])
                request.session['user_form'] = user_form.cleaned_data
                request.session['moreinfo_form'] = moreinfo_form
                return redirect('lawyersignup2')
        user_form = UserSignUpForm( prefix='form1')
        moreinfo_form= MoreUserInfoForm(prefix='form2')
        context = {'user_form':user_form,
                    'moreinfo_form':moreinfo_form,}
        return render (request,'lawyersignup1.html',context)
     except Exception as e:
                    return HttpResponse(f"Error Occurred: {e}")
    
def lawyersignup2(request):
    try:
        user_form = request.session.get('user_form')
        moreinfo_form = request.session.get('moreinfo_form')
        if not user_form or not moreinfo_form :
            return redirect('lawyersignup1')
        if request.method =="POST": 
            details_form = LawyerDetailsForm(request.POST)
            office_address_form = AddressForm(request.POST)
            if details_form.is_valid() and office_address_form.is_valid():
                request.session['details_form'] = details_form.cleaned_data
                request.session['office_address_form'] = office_address_form.cleaned_data 
                return redirect('lawyersignup3')
        office_address_form = AddressForm()
        details_form = LawyerDetailsForm()
        context = {'office_address_form':office_address_form,
                      'details_form':details_form,}
        return render (request,'lawyersignup2.html',context)
    except Exception as e:
                    return HttpResponse(f"Error Occurred: {e}")
    

def laywersignup3(request):
    try:
        user_form = request.session.get('user_form')
        moreinfo_form = request.session.get('moreinfo_form')
        details_form = request.session.get('details_form')
        office_address_form = request.session.get('office_address_form')

        if not user_form or not moreinfo_form or not details_form or not office_address_form:
            return redirect('lawyersignup1')
        
        if request.method == "POST":
            documents_form = LawyerDocumentsForm(request.POST, request.FILES, prefix='form5')
            if documents_form.is_valid():
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=user_form['username'],
                        first_name=user_form['first_name'],
                        last_name=user_form['last_name'],
                        email=user_form['email'],
                        password=user_form['password1']
                    )
                    
                    if 'dob' in moreinfo_form:
                        moreinfo_form['dob'] = deserialize_date(moreinfo_form['dob'])
                    
                    moreinfo, created = MoreUserInfo.objects.get_or_create(user=user, defaults=moreinfo_form)
                    if not created:
                        for attr, value in moreinfo_form.items():
                            setattr(moreinfo, attr, value)
                        moreinfo.save()
                    
                    address = Address.objects.create(user = user ,
                                                     **office_address_form)
                    lawyer_details = LawyerDetails.objects.create(
                        user=user,
                        office_address=address,
                        **details_form
                    )
                    
                    lawyer_documents = documents_form.save(commit=False)
                    lawyer_documents.user = user
                    lawyer_documents.save()
                    
                    more_user_info = MoreUserInfo.objects.get(user=user)
                    more_user_info.is_completed_for_lawyer = True
                    more_user_info.save()

                    request.session.flush()
                    return HttpResponse("Lawyer account created successfully")
    
        documents_form = LawyerDocumentsForm(prefix='form5')
        context = {'documents_form': documents_form}
        return render(request, 'lawyersignup3.html', context)
    
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")

         




def lawyer_login(request):
    print('run')
    if request.method == "POST":
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            print(user)
            status_check = LawyerDetails.objects.get(user=user)
            lawyer_check = LawyerDetails.objects.get(user=user)
            status = status_check.status
            is_lawyer = lawyer_check.is_lawyer
            print(status)
            if status == "approved" and is_lawyer:
                print(status)
                login(request,user)
                return HttpResponse (' lawyer login is successful')
    return render(request,'lawyerlogin.html')




































def test(request):
        user_form = request.session.get('user_form')
        moreinfo_form = request.session.get('moreinfo_form')
        if not user_form or not moreinfo_form :
            return redirect('lawyersignup1')
        if request.method =="POST": 
            details_form = LawyerDetailsForm(request.POST)
            office_address_form = AddressForm(request.POST)
            if details_form.is_valid() and office_address_form.is_valid():
                request.session['details_form'] = details_form.cleaned_data
                request.session['office_address_form'] = office_address_form.cleaned_data 
                return redirect('lawyersignup3')
        office_address_form = AddressForm()
        details_form = LawyerDetailsForm()
        context = {'office_address_form':office_address_form,
                      'details_form':details_form,}
        return render (request,'test.html',context)


#previous way of creating lawayerid
# def lawyersignup1(request):
#     try:
#         if request.method =="POST":
#             user_form = UserSignUpForm(request.POST ,prefix='form1')
#             moreinfo_form= MoreUserInfoForm(request.POST, prefix='form2')  
#             if user_form.is_valid() and moreinfo_form.is_valid():
#                 try:
#                         with transaction.atomic():
#                             user= user_form.save()#created user instance
#                             moreinfo_data = moreinfo_form.cleaned_data  # Get form data
#                             moreinfo, created = MoreUserInfo.objects.get_or_create(user=user, defaults=moreinfo_form)
#                             if not created:
#                                 # Update existing MoreUserInfo object if it already exists
#                                 for attr, value in moreinfo_data.items():
#                                     setattr(moreinfo, attr, value)
#                                 moreinfo.save()
#                             request.session['user_id'] = user.id
#                         return redirect('lawyersignup2')
#                 except IntegrityError:
#                         return HttpResponse("Error: Integrity Violation. User might already exist.")
#         user_form = UserSignUpForm( prefix='form1')
#         moreinfo_form= MoreUserInfoForm(prefix='form2')
#         context = {'user_form':user_form,
#                     'moreinfo_form':moreinfo_form,}
#         return render (request,'lawyersignup1.html',context)
#     except Exception as e:
#                     return HttpResponse(f"Error Occurred: {e}")
    
# def lawyersignup2(request):
#     try:
#         user_id = request.session.get('user_id')
#         if user_id is None:
#             return redirect('lawyersignup1')
#         if request.method =="POST": 
#             details_form = LawyerDetailsForm(request.POST)
#             office_address_form = AddressForm(request.POST)
#             if details_form.is_valid() and office_address_form.is_valid():
#                 address = office_address_form.save()
#                 #storing lawyer additional details
#                 lawyer_details = details_form.save(commit = False)
#                 lawyer_details.user =  User.objects.get(pk=user_id)
#                 lawyer_details.office_address = address
#                 lawyer_details.save()
#                 return redirect('lawyersignup3')
#         office_address_form = AddressForm()
#         details_form = LawyerDetailsForm()
#         context = {'office_address_form':office_address_form,
#                       'details_form':details_form,}
#         return render (request,'lawyersignup2.html',context)
#     except Exception as e:
#                     return HttpResponse(f"Error Occurred: {e}")
    
# def laywersignup3(request):
#     # try:
#             user_id = request.session.get('user_id')
#             if user_id is None:
#                 return redirect('lawyersignup1')
            
#             if request.method =="POST":
#                 documents_form = LawyerDocumentsForm(request.POST,request.FILES,prefix='form5')
#                 if documents_form.is_valid():
#                     try:
#                         #storing lawyer documents 
#                             lawyer_documents = documents_form.save(commit = False)
#                             user = get_object_or_404(User, pk=user_id)
#                             print(user)
#                             lawyer_documents.user =User.objects.get(pk=user_id)
#                             lawyer_documents.save()
#                             user = User.objects.get(pk=user_id)
#                             more_user_info= MoreUserInfo.objects.get(user=user)
#                             more_user_info.is_completed_for_lawyer = True  # or False, depending on your logic
#                             more_user_info.save()
#                             del request.session['user_id']
#                             return HttpResponse("lawayer account created successfully")
#                     except IntegrityError:
#                         return HttpResponse("Error: Integrity Violation. User might already exist.")
#             documents_form = LawyerDocumentsForm(prefix='form5')
#             context = {'documents_form':documents_form}
#             return render(request,'lawyersignup3.html',context)
#     # except Exception as e:
#     #     error_cause = type(e).__name__  # Get the type of the exception (e.g., ValueError, KeyError, etc.)
#     #     error_message = str(e)  # Get the error message as a string
#     #     return HttpResponse(f"Error Occurred: {error_cause}: {error_message}")   