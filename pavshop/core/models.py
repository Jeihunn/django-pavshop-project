from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


# Create your models here.


class AbstractModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

    class Meta:
        abstract = True


class Contact(AbstractModel):
    full_name = models.CharField(verbose_name=_("Full Name"), max_length=150)
    email = models.EmailField(verbose_name=_("Email"), max_length=50)
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"))
    subject = models.CharField(verbose_name=_("Subject"), max_length=100)
    message = models.TextField(verbose_name=_("Message"))

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return f"{self.subject} - {self.full_name}"


class Newsletter(AbstractModel):
    email = models.EmailField(verbose_name=_("Email"), max_length=50, unique=True)
    subscription_status = models.BooleanField(verbose_name=_("Subscription Status"), default=True)

    class Meta:
        verbose_name = _("Newsletter")
        verbose_name_plural = _("Newsletters")

    def __str__(self):
        return self.email
