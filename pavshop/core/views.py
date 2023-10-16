from django.shortcuts import render, redirect
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .forms import ContactForm
from django.views.generic import CreateView
from product.models import ProductVersion
from blog.models import Blog
from core.models import TeamMember
from random import sample
from core.tasks import (backgound_task_testing, send_email_to_subscribers)

# Create your views here.


def index_view(request):
    active_product_versions = ProductVersion.objects.filter(is_active=True)
    product_versions = active_product_versions.order_by("-created_at")[:8]
    if active_product_versions.count() < 3:
        random_product_versions = active_product_versions
    else:
        random_product_versions = sample(list(active_product_versions), 3)
    
    blogs = Blog.objects.filter(is_active=True).order_by("-created_at")[:2]

    context = {
        "product_versions": product_versions,
        "random_product_versions": random_product_versions,
        "blogs": blogs,
    }
    return render(request, "core/index.html", context)


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
    product_versions_count = ProductVersion.objects.filter(is_active=True).count()
    team_members = TeamMember.objects.filter(is_active=True).order_by("display_order")

    context = {
        "product_versions_count": product_versions_count,
        "team_members": team_members,
    }
    return render(request, "core/about-us.html", context)


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


def backgound_task_view(request):  # for testing celery
    send_email_to_subscribers.delay()
    backgound_task_testing.delay()
    return HttpResponse("All tasks submitted")
