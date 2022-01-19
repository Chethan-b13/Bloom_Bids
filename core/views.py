from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.views.generic import ListView, DetailView, View
from .models import Item, Order, CartItem, UserAddress
from .forms import AddressForm
# Create your views here.


class HomePage(ListView):
    model = Item
    context_object_name = 'Flowers'
    template_name = "index.html"


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Item
    context_object_name = 'Flower'
    template_name = "Product_detail.html"


@login_required(login_url='/login/')
def OrderSummary(request):
    cart_items, created = CartItem.objects.get_or_create(
        user=request.user, ordered=False)
    context = {'cart_items': cart_items}
    print(cart_items)
    return render(request, 'cart.html', context)


@login_required
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
            messages.success(request, "Added Quantity Item")
            return redirect("core:order-summary")
        else:
            cart_item.item.add(ordered_item)
            messages.success(request, "Added Item to your cart")
            return redirect("core:order-summary")

    else:
        ordered_date = timezone.now()
        cart_item = CartItem.objects.create(
            user=request.user, order_date=ordered_date)
        cart_item.item.add(ordered_item)
        messages.success(request, "Added Item to your cart")
        return redirect("core:order-summary", pk=pk)


@login_required
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
            messages.success(request, "Item \"" +
                             order_item.item.flower_name+"\" removed from your cart")
            return redirect("core:order-summary")
        else:
            messages.success(request, "This Item not in your cart")
            return redirect("core:order-summary")
    else:
        messages.success(request, "You do not have an Order")
        return redirect("core:order-summary")


@login_required
def remove_single_item_from_cart(request, pk):
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
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.success(request, "Cart Updated")
            return redirect("core:order-summary")

        else:
            messages.success(request, "This Item is not in your cart")
            return redirect("core:order-summary")
    else:
        messages.success(request, "You do not have an Order")
        return redirect("core:order-summary")


@login_required
def Checkout(request):
    if request.method == "POST":
        form = AddressForm(request.POST or None)
        cart_items = CartItem.objects.get(user=request.user, ordered=False)
        order = Order.objects.filter(user=request.user, ordered=False)
        if form.is_valid():
            Customer_name = form.cleaned_data.get('name')
            aprt_address = form.cleaned_data.get('address')
            card_no = form.cleaned_data.get('Card_no')
            cvv = form.cleaned_data.get('cvv')
            exp_month = form.cleaned_data.get('exp_month')
            exp_year = form.cleaned_data.get('exp_year')
            Customer_zip = form.cleaned_data.get('zip')
            Customer_email = form.cleaned_data.get('email')
            Customer_city = form.cleaned_data.get('city')
            Customer_state = form.cleaned_data.get('state')
            if str(card_no) == '6060-3344-4512-5555' and str(cvv) == '127':
                address = UserAddress(
                    user=request.user,
                    email=Customer_email,
                    city=Customer_city,
                    state=Customer_state,
                    address=aprt_address,
                    name=Customer_name,
                    zip=Customer_zip
                )
                address.save()
                cart_items.address = address

                order_items = cart_items.item.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                cart_items.ordered = True
                cart_items.save()

                messages.info(request, "Order Placed Successfully")
                return redirect("core:Home-Page")
            else:
                messages.error(request, "Invalid Payment details")
                return redirect('core:checkout')
        else:
            messages.error(request, form.errors)
            return redirect('core:checkout')
    else:
        adress_form = AddressForm()
        return render(request, 'checkout.html', {'Form': adress_form})


@login_required
def Add_to_Wishlist(request, pk):
    item = get_object_or_404(Item, pk=pk)
    WishlistItem, created = Order.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
        wishlist=False,
    )

    if WishlistItem:
        WishlistItem.wishlist = True
        WishlistItem.save()
        messages.info(request, "Item added to your whishlist")

        return redirect('core:wishlist')
    else:
        messages.info(request, "Item already in your whishlist")
        return redirect('core:wishlist')


def remove_from_Wishlist(request, pk):
    item = get_object_or_404(Item, pk=pk)

    WishlistItem = Order.objects.filter(
        item=item,
        user=request.user,
        ordered=False,
        wishlist=True,
    )[0]
    if WishlistItem:
        WishlistItem.wishlist = False
        WishlistItem.save()
        messages.info(request, "Item removed from your whishlist")

        return redirect('core:wishlist')
    else:
        messages.info(request, "Item already in your whishlist")
        return redirect('core:wishlist')


@login_required
def Wishlist(request):
    cart_items = Order.objects.filter(
        user=request.user, ordered=False, wishlist=True)
    context = {'items': cart_items}
    return render(request, 'wishlist.html', context)
