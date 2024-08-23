from django.urls import path
from .import views
urlpatterns=[
    path('lawyersignup1/',views.lawyersignup1,name='lawyersignup1'),
    path('lawyersignup2/',views.lawyersignup2,name='lawyersignup2'),
    path('lawyersignup3/',views.laywersignup3,name='lawyersignup3'),
    path('lawyerlanding/',views.lawyerlanding,name='lawyerlanding'),
    path('logout/',views.logout,name='logout'),
    path('test',views.test,name='test'),
    path('lawyersearch/', views.lawyersearch, name='lawyersearch'),
    path('lawyer/dataset/<int:lawyer_id>/', views.lawyer_profile_detail_dataset, name='lawyer_profile_detail_dataset'),
    path('lawyer/details/<int:lawyer_id>/', views.lawyer_profile_detail_details, name='lawyer_profile_detail_details'),
    path('lawyer_book/<int:lawyer_id>/', views.lawyer_book, name='lawyer_book'),
    path('see_bookings/', views.see_bookings, name='see_bookings'),
    path('send_meeting_link/<int:booking_id>/', views.send_meeting_link, name='send_meeting_link'),
    path('lawyer_settings/', views.lawyer_settings, name='lawyer_settings'),
    path('lawyer_settings/', views.lawyer_settings, name='lawyer_settings'),
    path('mark-as-completed/<int:booking_id>/', views.mark_as_completed, name='mark_as_completed'),
    

    # path('lawyerlogin/',views.lawyer_login,name='lawyerlogin'),
   
]
