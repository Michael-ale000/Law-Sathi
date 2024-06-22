from django.urls import path,include
from.import views

urlpatterns = [
    path('user_landingpage',views.user_landingpage,name = "newsportal"),
    path('usersignup/',views.usersignup,name = "usersignup"),
    path('userlogin/',views.userlogin,name = "userlogin"),
]