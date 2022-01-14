from typing import Generic
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item, Order, CartItem
# Create your views here.


class HomePage(ListView):
    model = Item
    context_object_name = 'Flowers'
    template_name = "index.html"


class ProductDetailView(DetailView):
    model = Item
    template_name = "product.html"
