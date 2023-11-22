from django.db import models
from django.urls import reverse
from django.conf import settings

import misaka

from groups.models import Group

from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()
# this will just connect hte current post to whoever is logged in as a user

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now = True)
    # 13:00 auto_now = True means we dont have to put in the time it will be done automatically when the user posts
    message = models.TextField()
    message_html = models.TextField(editable = False)
    group = models.ForeignKey(Group, related_name = 'posts', null = True, blank = True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message
    
    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        # 15:10 this is so if someone writes in a markdown so they put a link in their post, it doesn't look with like a
        # strange notation of brackets and stuff, it is supported from the html from misaka
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs = {'username':self.user.username, 'pk':self.pk})
    # 16:20 we will use primary key as a way to relete the posts back to the url
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']
        # every message is uniquely linked to a user