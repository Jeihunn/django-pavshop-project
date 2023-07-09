from django.contrib import admin
from .models import Contact, Newsletter
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.admin.widgets import AdminTextInputWidget


# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'phone_number':
            kwargs['widget'] = PhoneNumberPrefixWidget(
                attrs={'class': 'vTextField'})
            kwargs['widget'].widget = AdminTextInputWidget(
                attrs={'class': 'vTextField'})
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    pass