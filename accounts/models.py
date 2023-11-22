from django.db import models
from django.contrib import auth
# Create your models here.
class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        # basically we add an @ then the username when we print the string representation of the username
        # 6:00 just like on twitter
        return "@{}".format(self.username)
    # username is defined as an attribute that comes defined in auth.models.user (has basics like firstname, lastname, email, 
    # username, and possibly one more field, check documentation 6:00)
    # 6:00, basically we are not going to create our own model but use django's built in model for logging in and out (4:50)
    # 6:20 we will use auth.models.User to automatically set up a form so when someone is siging up to be a user
    # django will do the back end for us