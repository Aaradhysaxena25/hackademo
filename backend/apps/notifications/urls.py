"""URL patterns for the notifications app."""

from django.urls import path

from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="list"),
    path(
        "<uuid:notification_id>/read/",
        views.MarkReadView.as_view(),
        name="mark-read",
    ),
]
