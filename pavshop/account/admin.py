from django.contrib import admin
from .models import Country, City, Address, Position

from django.contrib.auth.admin import UserAdmin
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.admin.widgets import AdminTextInputWidget
from django.contrib.auth import get_user_model

User = get_user_model()


# Register your models here.


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "updated_at"]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
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
