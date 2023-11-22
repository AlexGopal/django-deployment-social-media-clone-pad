# GROUPS URLS.PY
from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path("", views.ListGroups.as_view(), name = 'all'),
    path("new/", views.CreateGroup.as_view(), name = 'create'),
    path('posts/in/<slug>/', views.SingleGroup.as_view(), name = 'single'),
    #2:30 this will say posts/in and then slugify the actual group name and then it will lead to the actual group
    path('posts/join/<slug>/', views.JoinGroup.as_view(), name = 'join'),
    path('posts/leave/<slug>/', views.LeaveGroup.as_view(), name = 'leave'),
]