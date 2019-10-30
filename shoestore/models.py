from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY_CHOICES = (
    ("S", "Shoes"),
    ("SW", "Sport wear"),
    ("OW", "Out wear"),
)
LABEL_CHOICES = (
    ("S", "primary"),
    ("S", "secondary"),
    ("D", "danger"),
)


class Item(models.Model):
    title = models.CharField(max_length=20)
    price = models.FloatField()
    image = models.ImageField(upload_to='shoe_images', blank=True, default='shoe_images/shoestore.jpg')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
