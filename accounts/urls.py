from django.urls import path
from django.contrib.auth import views as auth_views
# 5:40 explains why we do the special import but basically it's just to take care
# of the login and logout views so we dont have to make them ourselves and so we can also
# do the below import statement and not get confused
from . import views
# we do the 2nd line so we dont mix our own views up with the auth views

app_name = 'accounts'
# 5:50 we do this so if we want to use url templates in base.html 
# we can just refer it to as the account's application, a good example would be in the navagation bar
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name = 'accounts/login.html')
                                                , name = 'login'),
    #  7:00 the name = login is for url templates in the future
    path("logout/", auth_views.LogoutView.as_view(), name = "logout"),
    # for login view you must connect it to your template name but for logout view
    # there is a default view you can use (8:50)
    path("signup/", views.SignUp.as_view(), name = 'signup'),

]
