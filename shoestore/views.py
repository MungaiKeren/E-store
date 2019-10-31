from django.shortcuts import render, redirect
from .forms import *
from django.views.generic import ListView, DetailView


# Create your views here.
class HomeView(ListView):
    model = Item
    template_name = "index.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "products.html"


# def index(request):
#     title = "E-Store"
#     items = Item.objects.all()
#     context = {
#         "title": title,
#         "items": items,
#     }
#     return render(request, "index.html", context)


# def products(request):
#     items = Item.objects.all()
#     context = {
#         "items": items
#     }
#     return render(request, 'products.html', context)


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
