import imp
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.


def Signup(request):

    return render(request, 'signup.html')