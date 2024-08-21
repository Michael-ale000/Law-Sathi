from django.urls import path,include
from.import views

urlpatterns = [
    path('user_landingpage/',views.user_landingpage,name = "user_landingpage"),
    path('usersignup/',views.usersignup,name = "usersignup"),
    path('login/',views.user_login,name = "login"),
    path('logout/',views.logout,name = "logout"),
    path('',views.index,name = "index"),
    path('choose/',views.choose,name = "choose"),
    path('settings/',views.settings,name = "settings"),

]