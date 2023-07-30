from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm
from .models import City


# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('core:index_view'))

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful. Welcome!')
                return redirect(reverse_lazy('core:index_view'))
    else:
        form = LoginForm()

    context = {
        "form": form,
    }
    return render(request, "account/login.html", context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('core:index_view'))

    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Registration successful! You can now log in.")
            return redirect(reverse_lazy('account:login_view'))
    else:
        form = RegisterForm()

    context = {
        "form": form
    }
    return render(request, "account/register.html", context)


def logout_view(request):
    logout(request)
    return redirect('account:login_view')


def load_cities_view(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    city_choices = [
        (city.id, f"{city.name}, {city.country.name}") for city in cities]
    return JsonResponse(city_choices, safe=False)
