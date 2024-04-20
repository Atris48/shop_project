from django.urls import path
from . import views

urlpatterns = [
    path('chat-detail/<str:phone>', views.ChatDetailView.as_view(), name='chat_detail'),
    path('create-chat', views.CreateChatView.as_view(), name='create_chat'),
    path('admin-clear-chat/<int:pk>', views.AdminClearChat.as_view(), name='admin_clear_chat'),
]
