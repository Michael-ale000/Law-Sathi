from django.urls import path
from .import views
urlpatterns=[
    path('lawyersignup1',views.lawyersignup1,name='lawyersignup1'),
    path('lawyersignup2',views.lawyersignup2,name='lawyersignup2'),
    path('lawyersignup3',views.laywersignup3,name='lawyersignup3'),
    path('test',views.test,name='test'),
    path('login',views.test,name='login'),
   
]
