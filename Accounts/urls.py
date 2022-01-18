from django import urls
from django.urls import path
from .views import *

app_name = 'Accounts'

urlpatterns = [
    path('signup/', Signup, name="Signup"),
    path('login/', Login, name="Login"),
    path('logout/', Logout, name='Logout'),
]
