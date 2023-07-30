from django import forms
from .models import Contact
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ContactForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control'}))

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
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
        }