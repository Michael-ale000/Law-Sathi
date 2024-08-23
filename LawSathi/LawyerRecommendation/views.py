from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .form import UserSignUpForm,MoreUserInfoForm,AddressForm,LawyerDetailsForm,LawyerDocumentsForm,BookingForm,AddressUpdateForm
from django.db import transaction,IntegrityError
from NewsPortal.models import MoreUserInfo
from django.contrib.auth.models import User
from .models import Address,LawyerDetails,LawyerDocuments,Lawyerdataset,Booking
from datetime import date
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from itertools import chain
from django.conf import settings
from urllib.parse import urlparse, parse_qs
from NewsPortal.form import UserUpdateForm,MoreUserInfoUpdateForm
import os,requests
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
load_dotenv()

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
                messages.success(request,'Form Data Were Valid')
                return redirect('lawyersignup2')
            else :
                for field, errors in user_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
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
                messages.success(request,'Form Data Were Valid')
                return redirect('lawyersignup3')
            else :
                for field, errors in details_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
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
                    messages.success(request,'Form Submiteed Sucessfully. Wait For Conformation Mail.')
                    return redirect('login')
    
        documents_form = LawyerDocumentsForm(prefix='form5')
        context = {'documents_form': documents_form}
        return render(request, 'lawyersignup3.html', context)
    
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")

@login_required        
def lawyersearch(request):
    # Start with all LawyerDetails
    lawyer_details = LawyerDetails.objects.filter(status='approved')
    other_lawyers = Lawyerdataset.objects.all()
    # Apply search bar filter
    if 'search' in request.GET:
        search_query = request.GET['search']
        lawyer_details = lawyer_details.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )
        other_lawyers = other_lawyers.filter(
            Q(name__icontains=search_query)  # Adjust this according to the fields in OtherLawyerModel
        )

    # Filter by Experience
    if 'experience' in request.GET:
        experience_ranges = request.GET.getlist('experience')
        experience_q = Q()
        for range_str in experience_ranges:
            if '-' in range_str:  # For ranges like "0-5"
                min_exp, max_exp = map(int, range_str.split('-'))
                experience_q |= Q(experience__gte=min_exp, experience__lte=max_exp)
            elif '+' in range_str:  # For "25+"
                min_exp = int(range_str.rstrip('+'))
                experience_q |= Q(experience__gte=min_exp)
        
        lawyer_details = lawyer_details.filter(experience_q)
        other_lawyers = other_lawyers.filter(experience_q)

    # Filter by Case Completion Days
    if 'average_case_completion_days' in request.GET:
        completion_days_ranges = request.GET.getlist('average_case_completion_days')
        completion_q = Q()
        for days_str in completion_days_ranges:
            if days_str == '5':
                completion_q |= Q(average_case_completion_days__lt=30)
            elif days_str == '10':
                completion_q |= Q(average_case_completion_days__gte=30, average_case_completion_days__lte=60)
            elif days_str == '15':
                completion_q |= Q(average_case_completion_days__gte=60, average_case_completion_days__lte=90)
            elif days_str == '20':
                completion_q |= Q(average_case_completion_days__gte=90, average_case_completion_days__lte=120)
            elif days_str == '25':
                completion_q |= Q(average_case_completion_days__gte=120)

        lawyer_details = lawyer_details.filter(completion_q)
        other_lawyers = other_lawyers.filter(experience_q)

    if 'location' in request.GET:
        provinces = request.GET.getlist('location')  # Get a list of selected locations
        if provinces:
            lawyer_details = lawyer_details.filter(office_address__province__in=provinces)
            other_lawyers = other_lawyers.filter(province__in=provinces)

    combined_lawyers = list(chain(lawyer_details, other_lawyers))
    combined_lawyers.sort(key=lambda x: getattr(x, 'rating', getattr(x, 'Rating', 0)), reverse=True)
    
    return render(request, 'lawyersearch.html', {'lawyer_details': combined_lawyers,'MEDIA_URL': settings.MEDIA_URL })

@login_required
def lawyerlanding(request):
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

        return render(request, 'lawyerlanding.html', context)
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")

def logout(request):
    try:
        logout(request)
        messages.success(request,"Loged Out.")
        return redirect('login')  # Redirect to the home page or any other page
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")

# showing lawyer detaisl for view profile 
@login_required
def lawyer_profile_detail_dataset(request, lawyer_id):
    # try:
        lawyer = get_object_or_404(Lawyerdataset, id=lawyer_id)

        return render(request, 'lawyer_profile_detail.html', {'lawyer': lawyer,'MEDIA_URL': settings.MEDIA_URL})
    # except Exception as e:
    #     return HttpResponse(f"Error Occurred: {e}")

@login_required
def lawyer_profile_detail_details(request, lawyer_id):
    try:
        form = BookingForm()
        lawyer = get_object_or_404(LawyerDetails, user_id=lawyer_id)
        return render(request, 'lawyer_profile_detail.html', {'lawyer': lawyer , 'form':form})
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")



# lawyer booking
@login_required
def lawyer_book(request, lawyer_id):
    try:
        # Fetch the lawyer object based on the provided ID
        lawyer = get_object_or_404(LawyerDetails, user_id=lawyer_id)

        if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.lawyer = lawyer
                booking.client = request.user
                # Check if the lawyer is already booked for the same date and time
                existing_booking = Booking.objects.filter(
                    lawyer=lawyer,
                    date=booking.date,
                    time=booking.time
                ).exists()
                if existing_booking:
                    messages.error(request, 'This time slot is already booked. Please choose another.')
                    # Re-render the form with error messages
                    return render(request, 'lawyer_profile_detail.html', {'lawyer': lawyer, 'form': form})
                else:
                    booking.save()
                    messages.success(request, 'Booking successful!')
                    return redirect('user_landingpage')  # Redirect to a success page or another view
            else:
                # If the form is not valid, re-render the form with error messages
                for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f'{field}: {error}')
                return render(request, 'lawyer_profile_detail.html', {'lawyer': lawyer, 'form': form})
        else:
            # Create a form instance for GET request
            form = BookingForm()
            return render(request, 'lawyer_profile_detail.html', {'lawyer': lawyer, 'form': form})
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")

@login_required
def see_bookings(request):
    try:
        # Fetch the lawyer object
        lawyer = LawyerDetails.objects.filter(user=request.user).first()
        if request.method == 'POST':
        # Mark booking as completed
            booking_id = request.POST.get('booking_id')
            booking = Booking.objects.filter(id=booking_id, lawyer=lawyer).first()
            if booking:
                booking.status = 'completed'  # Assuming 'completed' is a valid status in your model
                booking.save()
                return redirect('see_bookings')

        
        # Fetch all bookings for the lawyer
        bookings = Booking.objects.filter(lawyer=lawyer).order_by('-date', '-time')
        
        # Render the bookings in a template
        return render(request, 'see_bookings.html', {'lawyer': lawyer, 'bookings': bookings})
    except Exception as e:
        return HttpResponse(f"Error Occurred: {e}")

@login_required
def send_meeting_link(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        meeting_link = request.POST.get('meeting_link')
        if meeting_link:
            booking.meeting_link = meeting_link
            url =meeting_link
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            room_id = query_params.get('roomID', [None])[0]
            booking.room_id = room_id
            booking.save()
            messages.success(request, 'Meeting link sent successfully!')
            
            print(room_id)
            return redirect('see_bookings')  # Adjust the redirect as needed

    return redirect('see_bookings')  # Redirect in case of GET request or other issues

@login_required
def mark_as_completed(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'completed'
    booking.meeting_link = ''  # Clear the meeting link
    booking.room_id =None
    booking.save()
    messages.success(request, 'Booking marked as completed and meeting link removed!')
    return redirect('see_bookings')

@login_required
def lawyer_settings(request):
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
            address_update_form = AddressUpdateForm(instance=request.user.address)
            user_form = UserUpdateForm(instance=request.user)
            more_user_info_form = MoreUserInfoUpdateForm(instance=request.user.moreuserinfo)

        context = {
        'user_form': user_form,
        'more_user_info_form': more_user_info_form,
        'address_update_form':address_update_form}
        return render(request,'lawyer_settings.html',context)
    except Exception as e:
        return HttpResponse(f"Error Occurred:{e}")


# def lawyer_login(request):
#     try:
#         if request.method == "POST":
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request,username=username,password=password)
#             if user is not None:
#                 try:
#                     status_check = LawyerDetails.objects.get(user=user)
#                     lawyer_check = LawyerDetails.objects.get(user=user)
#                     status = status_check.status
#                     is_lawyer = lawyer_check.is_lawyer
#                     if is_lawyer:
#                         if status == "approved":
#                             login(request,user)
#                             messages.success(request,'Loged In Successfully')
#                             return HttpResponse (' lawyer login is successful')
#                         else:
#                             messages.error(request,'Form Is Not Accepted. Wait For Conformation Mail.')
#                             return render(request,'lawyerlogin.html')

#                 except LawyerDetails.DoesNotExist:
#                     messages.error(request,'Your Are A General User. Login As A General User.')
#                     url = reverse('userlogin')
#                     return redirect(url)
#             messages.error(request,'Username or Password Is Invalid')
#         return render(request,'lawyerlogin.html')

#     except Exception as e:
#         return HttpResponse(f"Error Occurred: {e}")


































def test(request):
        return render (request,'test.html')


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