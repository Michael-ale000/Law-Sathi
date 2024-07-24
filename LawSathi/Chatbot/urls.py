from django.urls import path
from .views import chat_view,temp_view
urlpatterns=[ 
    path('chatbot/', chat_view, name='chatbot'),
    path('temp/', temp_view, name='temp'),
]
