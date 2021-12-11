from django import urls
from django.urls import path
from .views import *

app_name = 'core'


urlpatterns = [
    path("", HomePage.as_view(), name="Home-Page"),
    path(
        'product/<int:pk>',
        ProductDetailView.as_view(),
        name='Detail-view'
    ),
]
