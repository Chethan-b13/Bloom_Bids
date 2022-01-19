
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def Signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['FName']
        last_name = request.POST['LName']
        email = request.POST['Email_Id']
        pass_word = request.POST['Password']
        print(pass_word)
        if User.objects.filter(username=username).exists():
            messages.info(request, 'User with Username Already Exists')
            return redirect('Accounts:Signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Id Already Taken')
            return redirect('Accounts:Signup')
        else:
            user = User.objects.create_user(
                username=username, first_name=first_name, email=email, last_name=last_name, password=pass_word)
            user.save()
            return redirect('Accounts:Login')

    return render(request, 'signup.html')


def Login(request):
    if request.method == "POST":
        user_name = request.POST['username']
        pass_word = request.POST['password']
        print(user_name)
        print(pass_word)
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            messages.info(
                request, f'Hello {user.username} Welcome to Blush&Bloom')

            return redirect('core:Home-Page')
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('Accounts:Login')

    else:
        return render(request, 'login.html')


def Logout(request):
    # if request.method == 'POST':
    logout(request)
    messages.info(request, "See you Soon")
    return redirect('core:Home-Page')
