from django.urls import path,include
from.import views

urlpatterns = [
    path('',views.landingpage,name = "newsportal"),
    path('usersignup/',views.usersignup,name = "usersignup"),
]