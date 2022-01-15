from time import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from typing import Generic
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


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    ordered_item, created = Order.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    user_cartitem = CartItem.objects.filter(
        user=request.user, ordered=False)

    if user_cartitem.exists():
        cart_item = user_cartitem[0]

        if cart_item.item.filter(item__pk=item.pk).exists():
            ordered_item.quantity += 1
            ordered_item.save()
            messages.info(request, "Added Quantity Item")
            return redirect("core:Detail-view", pk=pk)
        else:
            cart_item.item.add(ordered_item)
            messages.info(request, "Added Item to your cart")
            return redirect("core:Detail-view", pk=pk)

    else:
        ordered_date = timezone.now()
        cart_item = CartItem.objects.create(
            user=request.user, order_date=ordered_date)
        cart_item.item.add(ordered_item)
        messages.info(request, "Added Item to your cart")
        return redirect("core:Detail-view", pk=pk)


def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    user_cartitems = CartItem.objects.filter(user=request.user,
                                             ordered=False
                                             )
    if user_cartitems.exists():
        cart_items = user_cartitems[0]

        if cart_items.item.filter(item__pk=item.pk).exists():
            order_item = Order.objects.filter(user=request.user,
                                              item=item,
                                              ordered=False)[0]
            order_item.delete()
            messages.info(request, "Item \"" +
                          order_item.item.flower_name+"\" remove from your cart")
            return redirect("core:Detail-view", pk=pk)
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("core:Detail-view", pk=pk)
    else:
        messages.info(request, "You do not have an Order")
        return redirect("core:Detail-view", pk=pk)
