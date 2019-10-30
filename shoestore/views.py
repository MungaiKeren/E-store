from django.shortcuts import render, redirect
from .forms import *


# Create your views here.
def index(request):
    title = "E-Store"
    context = {
        "title": title,
    }
    return render(request, "index.html", context)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signUp.html', {"form": form})
