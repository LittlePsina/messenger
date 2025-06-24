# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('chat/', views.chat_view, name='chat'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('user-search/', views.user_search, name='user-search'),
    path('chat/create/', views.create_chat, name='create_chat'),
]
