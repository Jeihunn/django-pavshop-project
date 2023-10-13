from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from core.models import AbstractModel, CustomImageField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Country(AbstractModel):
    name = models.CharField(verbose_name=_(
        "Name"), max_length=100, unique=True)
    country_code = models.CharField(verbose_name=_(
        "Country Code"), max_length=3, unique=True)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return f"{self.name} ({self.country_code})"


class City(AbstractModel):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities", verbose_name=_("Country"))

    name = models.CharField(verbose_name=_("Name"), max_length=100)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class Address(AbstractModel):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name=_("Country"))
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name=_("City"))

    street_address = models.CharField(
        verbose_name=_("Street Address"), max_length=250)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        address_str = f"{self.country.name} - {self.city.name} - {self.street_address}"
        if len(address_str) > 80:
            return f"{address_str[:80]}..."
        else:
            return address_str


class Position(AbstractModel):
    name = models.CharField(verbose_name=_(
        "Name"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")

    def __str__(self):
        return self.name


class User(AbstractUser):
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Address"))
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True,
                                 blank=True, related_name="users", verbose_name=_("Position"))

    bio = models.TextField(verbose_name=_("Bio"), null=True, blank=True)
    phone_number = PhoneNumberField(verbose_name=_(
        "Phone Number"), null=True, blank=True, unique=True)
    profile_image = CustomImageField(verbose_name=_(
        "Profile Image"), upload_to="profile_images", default="profile_images/default_profile.jpg")
    ips = models.JSONField(verbose_name=_(
        "Ips"), default=list, null=True, blank=True)


class Blacklist(AbstractModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("User"))

    ip_address = models.GenericIPAddressField(verbose_name=_(
        "IP Address"), protocol="both", unpack_ipv4=False, null=True, blank=True)
    start_time = models.DateTimeField(
        verbose_name=_("Start Time"), default=timezone.now)
    duration = models.DurationField(
        verbose_name=_("Duration"),
        help_text=_("Specify the duration in the format '45 days 15:29:40'."),
    )
    reason = models.TextField(verbose_name=_("Reason"), null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)

    class Meta:
        verbose_name = _("Blacklist Entry")
        verbose_name_plural = _("Blacklist Entries")

    def __str__(self):
        if self.user:
            return f"Blacklist for {self.user.username}"
        elif self.ip_address:
            return f"Blacklist for IP {self.ip_address}"
