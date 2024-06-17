from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .form import UserSignUpForm,MoreUserInfoForm,AddressForm,LawyerDetailsForm,LawyerDocumentsForm
from django.db import transaction,IntegrityError
from NewsPortal.models import MoreUserInfo
from django.contrib.auth.models import User


# Create your views here.
def lawyersignup1(request):
    try:
        if request.method =="POST":
            user_form = UserSignUpForm(request.POST ,prefix='form1')
            moreinfo_form= MoreUserInfoForm(request.POST, prefix='form2')  
            if user_form.is_valid() and moreinfo_form.is_valid():
                try:
                        with transaction.atomic():
                            user= user_form.save()#created user instance
                            moreinfo_data = moreinfo_form.cleaned_data  # Get form data
                            moreinfo, created = MoreUserInfo.objects.get_or_create(user=user, defaults=moreinfo_form)
                            if not created:
                                # Update existing MoreUserInfo object if it already exists
                                for attr, value in moreinfo_data.items():
                                    setattr(moreinfo, attr, value)
                                moreinfo.save()
                            request.session['user_id'] = user.id
                        return redirect('lawyersignup2')
                except IntegrityError:
                        return HttpResponse("Error: Integrity Violation. User might already exist.")
        user_form = UserSignUpForm( prefix='form1')
        moreinfo_form= MoreUserInfoForm(prefix='form2')
        context = {'user_form':user_form,
                    'moreinfo_form':moreinfo_form,}
        return render (request,'lawyersignup1.html',context)
    except Exception as e:
                    return HttpResponse(f"Error Occurred: {e}")
    
def lawyersignup2(request):
    try:
        user_id = request.session.get('user_id')
        if user_id is None:
            return redirect('lawyersignup1')
        if request.method =="POST": 
            details_form = LawyerDetailsForm(request.POST)
            office_address_form = AddressForm(request.POST)
            if details_form.is_valid() and office_address_form.is_valid():
                address = office_address_form.save()
                #storing lawyer additional details
                lawyer_details = details_form.save(commit = False)
                lawyer_details.user =  User.objects.get(pk=user_id)
                lawyer_details.office_address = address
                lawyer_details.save()
                return redirect('lawyersignup3')
        office_address_form = AddressForm()
        details_form = LawyerDetailsForm()
        context = {'office_address_form':office_address_form,
                      'details_form':details_form,}
        return render (request,'lawyersignup2.html',context)
    except Exception as e:
                    return HttpResponse(f"Error Occurred: {e}")
    
def laywersignup3(request):
    # try:
            user_id = request.session.get('user_id')
            if user_id is None:
                return redirect('lawyersignup1')
            
            if request.method =="POST":
                documents_form = LawyerDocumentsForm(request.POST,request.FILES,prefix='form5')
                if documents_form.is_valid():
                    try:
                        #storing lawyer documents 
                            lawyer_documents = documents_form.save(commit = False)
                            user = get_object_or_404(User, pk=user_id)
                            lawyer_documents.user =User.objects.get(pk=user_id)
                            lawyer_documents.save()
                            user.is_completed_forlawyer = True
                            user.save()
                            del request.session['user_id']
                            return HttpResponse("lawayer account created successfully")
                    except IntegrityError:
                        return HttpResponse("Error: Integrity Violation. User might already exist.")
            documents_form = LawyerDocumentsForm(prefix='form5')
            context = {'documents_form':documents_form}
            return render(request,'lawyersignup3.html',context)
    # except Exception as e:
    #     error_cause = type(e).__name__  # Get the type of the exception (e.g., ValueError, KeyError, etc.)
    #     error_message = str(e)  # Get the error message as a string
    #     return HttpResponse(f"Error Occurred: {error_cause}: {error_message}")            




def login(request):
      return render(request,'login.html')




































def test(request):
    if request.method =="POST":
            user_form = UserSignUpForm(request.POST ,prefix='form1')
            moreinfo_form= MoreUserInfoForm(request.POST, prefix='form2')  
            if user_form.is_valid() and moreinfo_form.is_valid():
                moreinfo_formdata = moreinfo_form.cleaned_data
                moreinfo_formdata['dob'] = moreinfo_formdata['dob'].strftime('%Y-%m-%d')  # Convert date to string
                request.session['user_formdata'] = user_form.cleaned_data
                request.session['moreinfo_formdata'] = moreinfo_formdata
                return redirect('lawyersignup2')
    user_form = UserSignUpForm( prefix='form1')
    moreinfo_form= MoreUserInfoForm(prefix='form2')
    context = {'user_form':user_form,
                    'moreinfo_form':moreinfo_form,}
    return render (request,'lawyersignup1.html',context)