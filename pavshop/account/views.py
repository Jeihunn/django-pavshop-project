from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm, RequestNewTokenForm, UpdateUserInfoForm
from .models import City
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from .utils import send_activation_email
from django.utils.translation import gettext_lazy as _

User = get_user_model()


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
                messages.success(request, _('Login successful. Welcome!'))
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
            user = form.save()

            send_activation_email(request, user)
            messages.info(
                request, _("Registration successful! Please confirm your email address to complete the registration. An activation link has been sent to your email."))
            return redirect(reverse_lazy('login_view'))
    else:
        form = RegisterForm()

    context = {
        "form": form,
    }
    return render(request, "account/register.html", context)


def user_profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "POST":
            form = UpdateUserInfoForm(
                data=request.POST, files=request.FILES, instance=user)
            if form.is_valid():
                if form.cleaned_data.get('set_to_default'):
                    user.profile_image = 'profile_images/default_profile.jpg'
                form.save()
            else:
                print(" ____________________________________ Form is not valid")
                print(form.errors)
        else:
            form = UpdateUserInfoForm(instance=user)
        context = {
            "form": form,
            "user": user,
        }
        return render(request, "account/user-profile.html", context)
    else:
        return redirect(reverse_lazy('core:index_view'))
   
    
def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('login_view'))


def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, _("Your account has been activated successfully. You can now log in."))
        return redirect(reverse_lazy('login_view'))
    else:
        return render(request, 'account/account_activation_invalid.html')


def request_new_token_view(request):
    if request.method == "POST":
        form = RequestNewTokenForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()

            send_activation_email(request, user)
            messages.info(
                request, _("An account activation token has been sent to your email address. Please check your inbox and follow the instructions to activate your account."))
            return redirect(reverse_lazy('login_view'))
    else:
        form = RequestNewTokenForm()

    context = {
        "form": form,
    }
    return render(request, "account/request_new_token.html", context)


def load_cities_view(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    city_choices = [
        (city.id, f"{city.name}, {city.country.name}") for city in cities]
    return JsonResponse(city_choices, safe=False)
