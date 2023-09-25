from django.shortcuts import render, redirect
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .forms import ContactForm
from django.views.generic import CreateView


# Create your views here.


def index_view(request):
    return render(request, "core/index.html")


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("Thank You. Your message has been sent successfully!"))
            return redirect(reverse_lazy("core:contact_view"))
        else:
            messages.error(
                request, _("Oops! Something went wrong. Please review your message and make sure all the required fields are filled correctly."))
    else:
        form = ContactForm()

    context = {
        "form": form,
    }
    return render(request, "core/contact.html", context)


def about_us_view(request):
    return render(request, "core/about-us.html")


# ===== Generic Views =====

class ContactView(CreateView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy("core:contact_view")

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user

        if user.is_authenticated:
            initial['full_name'] = user.get_full_name()
            initial['email'] = user.email

        return initial

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.add_message(self.request, messages.SUCCESS,
                             _("Successfully sent!"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _(
            "Oops! Something went wrong. Please review your message and make sure all the required fields are filled correctly."))
        return super().form_invalid(form)
