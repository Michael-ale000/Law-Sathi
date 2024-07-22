from django.urls import path
from .import views
urlpatterns=[
    path('dashboard/',views.dashboard,name='dashboard'),
    path('lawyer_videocall/',views.lawyer_videocall, name='lawyer_videocall'),
    path('user_videocall/',views.user_videocall, name='user_videocall'),
    path('join/',views.join_room, name='join_room'),

]
