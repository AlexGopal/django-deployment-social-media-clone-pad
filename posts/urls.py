from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("", views.PostList.as_view(), name = 'all'),
    path("posts/new/", views.CreatePost.as_view(), name = 'create'),
    path("by/<username>/",views.UserPosts.as_view(),name = "for_user"),
    path("by/<username>/<int:pk>/",views.PostDetail.as_view(),name = "single"),
    path("delete/<int:pk>/", views.DeletePost.as_view(), name = "delete"),
]

# 19:30 if get_context data or  get_queryset in post's views.py was hard to understand see documentation
# you will use these methods more as you get more advanced with Django
# you can use class based views without these methods but its only when you start getting more advanced or want extra
# funactionality will you end up adding one extra methods
# but alot of functionality we'll use for our own projects will probably at the start work just fine with class bsaed views
