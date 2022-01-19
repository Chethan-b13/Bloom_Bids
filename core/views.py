from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.views.generic import ListView, DetailView, View
from .models import Item, Order, CartItem, UserAddress, Payment
from .forms import AddressForm
import stripe
stripe.api_key = settings.STRIPE_KEY
# Create your views here.


class HomePage(ListView):
    model = Item
    context_object_name = 'Flowers'
    template_name = "index.html"


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Item
    context_object_name = 'Flower'
    template_name = "Product_detail.html"


class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            cart_items = CartItem.objects.get(
                user=self.request.user, ordered=False)
            context = {'cart_items': cart_items}
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.success(self.request, "No Products in the cart")
            return redirect('/')


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


def Checkout(request):
    if request.method == "POST":
        form = AddressForm(request.POST or None)
        order = CartItem.objects.get(user=request.user, ordered=False)
        if form.is_valid():
            Customer_name = form.cleaned_data.get('name')
            aprt_address = form.cleaned_data.get('address')
            Customer_country = form.cleaned_data.get('country')
            Customer_zip = form.cleaned_data.get('zip')
            Customer_email = form.cleaned_data.get('email')
            Customer_city = form.cleaned_data.get('city')
            Customer_state = form.cleaned_data.get('state')

            address = UserAddress(
                user=request.user,
                email=Customer_email,
                city=Customer_city,
                state=Customer_state,
                address=aprt_address,
                name=Customer_name,
                country=Customer_country,
                zip=Customer_zip
            )
            address.save()
            order.address = address
            order.save()
            return redirect('core:checkout')
    else:
        # if UserAddress.objects.get(user=request.user):
        #     messages.info(
        #         request, "Address Already Exists ! Redirecting to Payment")
        #     return redirect('core:checkout')
        # else:
        adress_form = AddressForm()
        return render(request, 'checkout.html', {'Form': adress_form})


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


def Wishlist(request):
    cart_items = Order.objects.filter(
        user=request.user, ordered=False, wishlist=True)
    context = {'items': cart_items}
    return render(request, 'wishlist.html', context)


# class PaymentView(View):
#     def get(self, *args, **kwargs):
#         order = CartItem.objects.get(user=self.request.user, ordered=False)
#         context = {
#             'order': order
#         }
#         return render(self.request, "payment.html", context)

#     def post(self, *args, **kwargs):
#         order = CartItem.objects.get(user=self.request.user, ordered=False)
#         token = self.request.POST.get('stripeToken')
#         amount = int(order.get_total_price() * 100)  # cents

#         try:
#             charge = stripe.Charge.create(
#                 amount=amount,
#                 currency="usd",
#                 source=token
#             )

#             # create payment
#             payment = Payment()
#             payment.stripe_id = charge['id']
#             payment.user = self.request.user
#             payment.amount = order.get_total_price()
#             payment.save()

#             # assign payment to order
#             order.ordered = True
#             order.payment = payment
#             order.save()

#             messages.success(self.request, "Success make an order")
#             return redirect('/')

#         except stripe.error.CardError as e:
#             body = e.json_body
#             err = body.get('error', {})
#             messages.error(self.request, f"{err.get('message')}")
#             return redirect('/')

#         except stripe.error.RateLimitError as e:
#             # Too many requests made to the API too quickly
#             messages.error(self.request, "To many request error")
#             return redirect('/')

#         except stripe.error.InvalidRequestError as e:
#             # Invalid parameters were supplied to Stripe's API
#             messages.error(self.request, "Invalid Parameter")
#             return redirect('/')

#         except stripe.error.AuthenticationError as e:
#             # Authentication with Stripe's API failed
#             # (maybe you changed API keys recently)
#             messages.error(self.request, "Authentication with stripe failed")
#             return redirect('/')

#         except stripe.error.APIConnectionError as e:
#             # Network communication with Stripe failed
#             messages.error(self.request, "Network Error")
#             return redirect('/')

#         except stripe.error.StripeError as e:
#             # Display a very generic error to the user, and maybe send
#             # yourself an email
#             messages.error(self.request, "Something went wrong")
#             return redirect('/')

#         except Exception as e:
#             # Something else happened, completely unrelated to Stripe
#             messages.error(self.request, "Not identified error")
#             return redirect('/')
