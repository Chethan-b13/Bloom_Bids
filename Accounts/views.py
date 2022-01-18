import imp
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import auth
# Create your views here.


def Signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['FName']
        last_name = request.POST['LName']
        email = request.POST['Email_Id']
        password = request.POST['Password']

        if User.objects.filter(username=username).exists():
            messages.danger('User with Username Already Exists')
            return redirect('Accounts:Signup')
        elif User.objects.filter(email=email).exists():
            messages.danger('Email Id Already Taken')
            return redirect('Accounts:Signup')
        else:
            user = User.objects.create(
                username=username, first_name=first_name, last_name=last_name, password=password)
            user.save()
            return redirect('Accounts:Login')

    return render(request, 'signup.html')


def Login(request):
    if request.method == "Post":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('core:Home-Page')
        else:
            messages.danger("Invalid Credentials")
    else:
        return render(request, 'login.html')


def Logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('core:Home-Page')
