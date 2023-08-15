from django.contrib import admin
from .models import Contact, Newsletter
from django.contrib.admin.models import LogEntry
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.admin.widgets import AdminTextInputWidget


# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "full_name", "email", "phone_number", "created_at", "updated_at"]
    list_display_links = ["id", "subject"]
    list_filter = ["created_at"]
    search_fields = ["subject", "full_name", "email", "phone_number"]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'phone_number':
            kwargs['widget'] = PhoneNumberPrefixWidget(
                attrs={'class': 'vTextField'})
            kwargs['widget'].widget = AdminTextInputWidget(
                attrs={'class': 'vTextField'})
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "subscription_status", "created_at", "updated_at"]
    list_display_links = ["id", "email"]
    list_editable = ["subscription_status"]
    list_filter = ["subscription_status", "created_at", "updated_at"]
    search_fields = ["email"]


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ["action_time", "user", "content_type", "object_id", "object_repr", "action_flag"]
    list_filter = ["action_time", "user", "action_flag"]