from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# what slugify does is it allows us to remove any characters
# that aren't alphanumeric, underscore, or hyphens
# 1:01 the idea is basically if you have a string that has spaces and
# you want to use it as part of the url, its going to be able to lowercase and add dashes instaed of spaces
# that way it works with your browser
import misaka
# 1:10 allows us to put links or markdown text, like reddit
from django.contrib.auth import get_user_model
User = get_user_model()
# 2:10 this allows us to call thing off of the current user's session
from django import template
register = template.Library()
# 2:40 this will be explained later but it is how you can use custom template tags

class Group(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    slug = models.SlugField(allow_unicode = True, unique = True)
    #6:00 explains what slug is but i think it's just for no mistakes when calling the url code
    description = models.TextField(blank = True, default = '')
    description_html = models.TextField(editable = False, default = '', blank = True)
    # 7:20 we may want an html version of our description
    members = models.ManyToManyField(User, through = 'GroupMember')
    # 10:40 many to many field is just all the members that belong to this group

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # 8:30 this means we can have spaces in the name but when we actually save it
        # the slug will become the slugify on self.name which just replaces and lowercases things
        self.description_html = misaka.html(self.description)
        # 9:00 incase we have markdown in the description i can call it with my html
        super().save(*args, **kwargs) 
    
    def get_absolute_url(self):
        return reverse('groups:single', kwargs = {'slug':self.slug})
    
    class Meta:
        ordering = ['name']
        

class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name = 'memberships', on_delete = models.CASCADE)
    # 4:00 tis means the groupmember is related to the group class through the foreign key
    user = models.ForeignKey(User, related_name='user_groups',on_delete = models.CASCADE)
    # 4:18 we get the user from the User = get_user_model()

    def __str__(self):
        return self.user.username
    
    class Meta:
        unique_together = ('group', 'user')