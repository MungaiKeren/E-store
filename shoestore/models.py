from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
import math


# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=20)
    goods = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


CATEGORY_CHOICES = (
    ("CL", "Casuals"),
    ("BT", "Boots"),
    ("OF", "Official"),
    ("CS", "Closed shoes"),
    ("OS", "Open shoes"),
    ("SW", "Sport wear"),
    ("OW", "Out wear"),
)
LABEL_CHOICES = (
    ("S", "primary"),
    ("S", "secondary"),
    ("D", "danger"),
)


class Item(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='shoe_images', blank=True, default='shoe_images/shoestore.jpg')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, blank=True)
    description = models.TextField()
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category']

    @classmethod
    def search_by_category(cls, search_term):
        searched_item = cls.objects.filter(category__icontains=search_term)
        return searched_item

    def get_absolute_url(self):
        return reverse("product", kwargs={
            "slug": self.slug
        })

    def add_to_cart_url(self):
        return reverse("add_to_cart", kwargs={
            "slug": self.slug
        })

    def remove_from_cart_url(self):
        return reverse("remove_from_cart", kwargs={
            "slug": self.slug
        })


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.name}'

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return math.ceil(self.get_total_item_price() - self.get_total_discount_item_price())

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
