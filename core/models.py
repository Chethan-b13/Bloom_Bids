from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
from django_countries.fields import CountryField
# Create your models here.

label_choices = (
    ('N', 'New'),
    ("Bs", "BestSeller")
)


# class UserInfo(models.Model):
#     """Model definition for UserInfo."""

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     email = models.EmailField(max_length=254)
#     Phone_number = models.models.CharField(max_length=12)

#     class Meta:
#         """Meta definition for UserInfo."""
#         verbose_name_plural = 'UserInfos'

#     def __str__(self):
#         """Unicode representation of UserInfo."""
#         return self.user.username


class UserAddress(models.Model):
    """Model definition for UserAddress."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=254, null=True)
    address = models.CharField(max_length=75)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)

    country = CountryField(multiple=False)

    class Meta:
        """Meta definition for UserAddress."""

        verbose_name = 'UserAddress'
        verbose_name_plural = 'UserAddresss'

    def __str__(self):
        """Unicode representation of UserAddress."""
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name


class Item(models.Model):
    flower_name = models.CharField(max_length=100, default="")
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=label_choices,
                             default="", max_length=2, blank=True, null=True)
    item_image = models.ImageField(
        upload_to="uploads/", default='/images/no-image.jpg')
    is_auctioned = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Items'

    def save(self, *args, **kwargs):
        if self.item_image:
            super().save(*args, **kwargs)
            img = Image.open(self.item_image.path)
            if img.height > 300 or img.width > 300:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.item_image.path)

    def __str__(self):
        return self.flower_name

    def get_absolute_url(self):
        return reverse("core:Detail-view", kwargs={"pk": self.pk})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={'pk': self.pk})

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={'pk': self.pk})

    def get_reduce_quantity_item_url(self):
        return reverse("core:reduce-quantity-item", kwargs={'pk': self.pk})


class Order(models.Model):
    """Model definition for CartItem."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    wishlist = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        """Meta definition for CartItem."""
        verbose_name_plural = 'Orders'

    def __str__(self):
        """Unicode representation of Orders."""
        return f"{self.quantity} of {self.item.flower_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()


class CartItem(models.Model):
    """Model definition for CartItems."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Order)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    order_address = models.ForeignKey(
        UserAddress, on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)

    class Meta:
        """Meta definition for CartItem."""

        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'

    def __str__(self):
        """Unicode representation of CartItem."""
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_item in self.item.all():
            total += order_item.get_total_item_price()
        return total

    def get_amount_saved(self):
        total = 0
        for order_item in self.item.all():
            total += order_item.get_amount_saved()
        return total

    def price_afted_saved(self):
        total = 0
        for order_item in self.item.all():
            total += order_item.get_final_price()
        return total


class Payment(models.Model):
    stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
