from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin, 
                                        PermissionRequiredMixin)
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic

from groups.models import Group, GroupMember
from . import models

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group
    # 1:40 for a create view we need to specifcy the fields they should be able to create
    # and link it up to the model


class SingleGroup(generic.DetailView):
    # this will just be details of a specific group like the posts inside the group
    model = Group
    # just link it up to the model for a detailview

# when someone goes to the listgroups page they will see a list of all the available groups
# its like a list of subreddits
class ListGroups(generic.ListView):
    model = Group
    # just need to link it up to the model
    
# 1:10 a person should be logged in to join a group and when someone clicks on join
# we do stuff on the back end of our models to join the actual user to be a group member of that group and then
# redirect to another page
class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs = {'slug':self.kwargs.get('slug')})
        # 2:30 basically get the slug for the page we're clicking the button of the join group of
        # 2:00 groups:single is the detail view of that group
        # 2:10 to know which groups we're talking about we add in kwargs

    # this method is just to make sure the person gets an error if they already a member of the group
    # so we try to create a new member, if they are member already tell them they are, if they arent a member
    # make them a member and tell them they became a member using django messages
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug = self.kwargs.get('slug'))
        # 3:05 try to get the group this person is looking at or return a 404 page, is what the above line does
        
        # 4:20 try to create a group member where user is the current user and group is the group
        # thats what the line under the try does
        try:
            GroupMember.objects.create(user = self.request.user, group = group)
            # basically the above line creates a group member
        
        except IntegrityError:
            messages.warning(self.request, ('Warning already a member!'))

        else:
            messages.success(self.request, ('You are now a member!'))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs = {'slug':self.kwargs.get('slug')})

    # make sure they cant leave a group if they arent in it
    def get(self, request, *args, **kwargs):
        try:
            # 8:40 try to get a membership off the group member assuming the user is
            # already in that group,
            membership = models.GroupMember.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get('slug')
                ).get()
        # expect if the member wasn't actually a member of that group
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, 'Sorry you are not in this group!')
        # if everything is working then delete the user from the group
        else:
            membership.delete()
            messages.success(self.request, 'You have left the group!')
        return super().get(request, *args, **kwargs)
        
        
