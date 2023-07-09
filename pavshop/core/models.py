from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Contact(AbstractModel):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=50)
    phone_number = PhoneNumberField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.subject


class Newsletter(AbstractModel):
    email = models.EmailField(max_length=50, unique=True)
    subscription_status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"

    def __str__(self):
        return self.email
