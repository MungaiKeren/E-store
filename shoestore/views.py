from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.views.generic import ListView, DetailView
from django.utils import timezone


# Create your views here.
class HomeView(ListView):
    model = Item
    template_name = "index.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "products.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
        else:
            # render a message saying that the order does not contain this order item
            return redirect("products", slug=slug)
    else:
        # should add a message saying the user doesn't have an order
        return redirect("product", slug=slug)
    return redirect("product", slug=slug)


def checkout(request):
    context = {

    }
    return render(request, 'checkout.html', context)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signUp.html', {"form": form})
