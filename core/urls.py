from django import urls
from django.urls import path
from .views import *

app_name = 'core'


urlpatterns = [
    path("", HomePage.as_view(), name="Home-Page"),
    path(
        'product/<int:pk>/',
        ProductDetailView.as_view(),
        name='Detail-view'
    ),
    path('order-summary/', OrderSummary.as_view(), name='order-summary'),
    path('add-to-cart/<int:pk>', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<int:pk>', remove_from_cart, name="remove-from-cart")
]
