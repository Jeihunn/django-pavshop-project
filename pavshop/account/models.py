from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from core.models import AbstractModel
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class Country(AbstractModel):
    name = models.CharField(max_length=100, unique=True)
    country_code = models.CharField(max_length=3, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name} ({self.country_code})"


class City(AbstractModel):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities")

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class Address(AbstractModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    street_address = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        address_str = f"{self.country.name} - {self.city.name} - {self.street_address}"
        if len(address_str) > 80:
            return f"{address_str[:80]}..."
        else:
            return address_str


class Position(AbstractModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"

    def __str__(self):
        return self.name


class User(AbstractUser):
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")

    bio = models.TextField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    profile_image = models.ImageField(
        upload_to="profile_images", default="profile_images/default_profile.jpg")
    ips = models.JSONField(default=list, null=True, blank=True)


class Blacklist(AbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(protocol="both", unpack_ipv4=False, null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    duration = models.DurationField()
    reason = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Blacklist Entry"
        verbose_name_plural = "Blacklist Entries"

    def __str__(self):
        if self.user:
            return f"Blacklist for {self.user.username}"
        elif self.ip_address:
            return f"Blacklist for IP {self.ip_address}"