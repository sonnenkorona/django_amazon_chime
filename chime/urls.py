from django.urls import path
from . import views

app_name = "meeting"
urlpatterns = [
  path("create/", views.MeetingCreateView.as_view(),name="create"),
  path("", views.MeetingListView.as_view(),name="list"),
  path("<str:pk>/", views.MeetingDetailView.as_view(),name="detail"),
  path("start/<str:pk>/", views.MeetingView.as_view(),name="meeting"),
]