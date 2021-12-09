from django import urls
from django.urls import path
from .views import *

app_name = 'core'


urlpatterns = [
    path("", Homepage.as_view(), name="Home-Page")
]
