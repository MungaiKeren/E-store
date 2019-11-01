from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib import messages


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
            messages.info(request, "This quantity was updated")
        else:
            messages.info(request, "Successfully added to cart")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Successfully added to cart")
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
            messages.info(request, "This item was removed from cart")
            return redirect("product", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product", slug=slug)
    else:
        # should add a message saying the user doesn't have an order
        messages.info(request, "You do not have an active order")
        return redirect("product", slug=slug)


def search_results(request):
    if 'category' in request.GET and request.GET['category']:
        search_term = request.GET.get('category')
        searched_items = Item.search_by_category(search_term)
        message = f'{search_term}'

        context = {
            "message": message,
            "items": searched_items
        }
        return render(request, 'search.html', context)
    else:
        message = "Item was not found"
        return render(request, 'search.html', {"message": message})


def checkout(request):
    context = {

    }
    return render(request, 'checkout.html', context)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Successfully registered")
        return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signUp.html', {"form": form})
