from django.urls import path
from .import views
urlpatterns=[ 
    path('chatbot/', views.chat_view, name='chatbot'),
    # path('temp/', temp_view, name='temp'),
    path('report/', views.report, name='report'),
    path('dashboard-data/', views.dashboard_data, name='dashboard_data'),
]
