from django.shortcuts import render
from django.urls import reverse_lazy
from . import forms
from django.views.generic import CreateView
# Create your views here.
# 7:00 reverse_lazy is basically just for the case that if someone is logged in or logged out where
# should they actually go
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    # 14:00 when someone successfully signs up for our website we want to bring them back to the login page
    # it's reverse_lazy because we dont want to do it until they hit submit
    template_name = 'accounts/signup.html'