"""URL patterns for the chat app."""

from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("conversations/", views.ConversationListView.as_view(), name="conversation_list"),
    path("conversations/<uuid:pk>/", views.ConversationDetailView.as_view(), name="conversation_detail"),
    path("conversations/<uuid:pk>/messages/", views.SendMessageView.as_view(), name="send_message"),
    path("conversations/<uuid:pk>/messages/list/", views.MessageListView.as_view(), name="message_list"),
]
