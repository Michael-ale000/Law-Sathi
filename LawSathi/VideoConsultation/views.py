from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def dashboard(request):
    return render(request, 'dashboard.html')


def lawyer_videocall(request):
    return render(request, 'lawyer_videocall.html')

def user_videocall(request):
    return render(request, 'user_videocall.html')

def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/user_videocall?roomID=" + roomID)
    return render(request, 'joinroom.html')

# def join_room1(request):
#     return render(request, 'joinroom1.html')