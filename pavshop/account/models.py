from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import AbstractModel
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class Country(AbstractModel):
    name = models.CharField(max_length=100, unique=True)
    country_code = models.CharField(max_length=2, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class City(AbstractModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Address(AbstractModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    street_address = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        if len(self.street_address) > 20:
            return f"{self.country} - {self.city} - {self.street_address[:20]}..."
        else:
            return f"{self.country} - {self.city} - {self.street_address}"


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
        Position, on_delete=models.SET_NULL, null=True, blank=True)

    bio = models.TextField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    profile_image = models.ImageField(
        upload_to="profile_images", default="profile_images/default_profile.jpg")
