from django import forms
from .models import Contact, SubBanner
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


# ========== Admin Forms ==========
class SubBannerAdminForm(forms.ModelForm):
    class Meta:
        model = SubBanner
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["breadcrumbs_en"].widget.attrs["placeholder"] = "Breadcrumb1 > Breadcrumb2 > ..."
        self.fields["breadcrumbs_az"].widget.attrs["placeholder"] = "Breadcrumb1 > Breadcrumb2 > ..."
# ========== END Admin Forms ==========


class ContactForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={"class": "form-control"}))

    class Meta:
        model = Contact
        fields = (
            "full_name",
            "email",
            "phone_number",
            "subject",
            "message",
        )
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
            }),
            "subject": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            }),
        }
