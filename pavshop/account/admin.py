from django.contrib import admin
from .models import Country, City, Address, Position, Blacklist
from .forms import BlacklistAdminForm
from django.contrib.auth.admin import UserAdmin
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.admin.widgets import AdminTextInputWidget
from django.contrib.auth import get_user_model

User = get_user_model()


# Register your models here.


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country_code", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "country_code"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    list_filter = ["country"]
    search_fields = ["name", "country__name"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["id", "country", "city",
                    "street_address", "created_at", "updated_at"]
    list_display_links = ["id", "country", "city", "street_address"]
    list_filter = ["country", "city"]
    search_fields = ["country__name", "country__country_code",
                     "city__name", "street_address"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["id", "username", "email", "first_name",
                    "last_name", "position", "is_active", "is_staff", "is_superuser"]
    list_display_links = ["id", "username"]
    list_filter = ["is_active", "is_staff", "is_superuser", "position"]
    search_fields = ["username", "email",
                     "first_name", "last_name", "phone_number"]
    ordering = ["-date_joined"]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email',
         'address', 'position', 'bio', 'phone_number', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'phone_number':
            kwargs['widget'] = PhoneNumberPrefixWidget(
                attrs={'class': 'vTextField'})
            kwargs['widget'].widget = AdminTextInputWidget(
                attrs={'class': 'vTextField'})
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    form = BlacklistAdminForm
    list_display = ["id", "user", "ip_address", "formatted_start_time", "duration", "is_active", "formatted_created_at", "formatted_updated_at"]
    list_filter = ["is_active", "start_time", "user", "ip_address"]
    search_fields = ["user__username", "ip_address", "reason"]

    def formatted_start_time(self, obj):
        return obj.start_time.strftime("%d/%m/%Y %H:%M:%S")
    formatted_start_time.admin_order_field = "start_time"
    formatted_start_time.short_description = "Start Time"

    def formatted_created_at(self, obj):
        return obj.created_at.strftime("%d/%m/%Y %H:%M:%S")
    formatted_created_at.admin_order_field = "created_at"
    formatted_created_at.short_description = "Created At"

    def formatted_updated_at(self, obj):
        return obj.updated_at.strftime("%d/%m/%Y %H:%M:%S")
    formatted_updated_at.admin_order_field = "updated_at"
    formatted_updated_at.short_description = "Updated At"