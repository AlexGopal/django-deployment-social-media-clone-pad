#POST VIEWS.PY
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()
# 2:30 basically the get_user_model import allows us to set a user object = to get_user_model
# and then call get_user_model, so if someone is logged into a session i can use the user object as
# the current user and then call things off of that
# Create your views here.
# 18:10 class postlist shows a list of posts related to either the user or the group
class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    # connect to the model
    select_related = ('user', 'group')
    # 3:30 this is a mixin that allows us to provide a tuple of related models which is the foreigne keys for this post
class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact = self.kwargs.get('username'))
            # 4:50 the prefetch_related is another method we can call off objects, see documentation
            # 5:30 basically we try to get the queryset which means it trys to set self.post.user that belongs to the post
            # to that user's object, then we will prefetch_related posts and get whereever the username is equal to the username
            # off who ever is logged in or whatever user you click on
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
        # all this method does is to make sure when you call the queryset for the user that the user actually exists
        # if they user doenst expect return  404 error, if the user does exist then just return a list of the user's posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        context['post_user'] = self.post_user
        return context
    # 7:38 return the context data object connected to whoever actually posted that specific user

class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact = self.kwargs.get('username'))
    # 9:20 similar to before, get the queryset for the actual post, and then filter where the username is equal to the
    # exact user's username, which us the username of the model's object

class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ('message', 'group')
    model = models.Post

    def form_valid(self,form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        # 11:00 the right hand side of the = means the user that sent the request
        self.object.save()
        # 11:00 we are trying to connect the post to the user
        return super().form_valid(form)
    
class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')
    # 12:00 once we  delete the post go back to the list of all the posts

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)
    
    def delete(self,*args,**kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)
    # 13:30 alot of the stuff we do for delete view is a convention and not chosen  can look this up
    # in the documentation

