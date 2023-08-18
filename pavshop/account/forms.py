from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm
)
from .models import Country, City, Address, Blacklist
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class BlacklistAdminForm(forms.ModelForm):
    class Meta:
        model = Blacklist
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        ip_address = cleaned_data.get('ip_address')

        if not user and not ip_address:
            raise forms.ValidationError({
                'user': [_("Both User and IP Address fields cannot be left empty at the same time. Please either select a User or provide an IP Address.")],
                'ip_address': [_("Both User and IP Address fields cannot be left empty at the same time. Please either select a User or provide an IP Address.")]
            })

        if user and ip_address:
            raise forms.ValidationError({
                'user': [_("You cannot select both a User and provide an IP Address at the same time. Please either select a User or provide an IP Address.")],
                'ip_address': [_("You cannot select both a User and provide an IP Address at the same time. Please either select a User or provide an IP Address.")]
            })


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(),
        required=True
    )

    first_name = forms.CharField(
        max_length=40, widget=forms.TextInput(),
        required=True
    )

    last_name = forms.CharField(
        max_length=40, widget=forms.TextInput(),
        required=True
    )

    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(attrs={"class": "form-control"}),
        required=True
    )

    street_address = forms.CharField(
        max_length=250,
        widget=forms.TextInput(),
        required=True
    )

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label="Select a country",
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Select a city",
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "street_address",
            "country",
            "city",
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _("A user with that email already exists."))
        return email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)

        street_address = self.cleaned_data["street_address"]
        country = self.cleaned_data["country"]
        city = self.cleaned_data["city"]

        address, _ = Address.objects.update_or_create(
            country=country,
            city=city,
            street_address=street_address
        )

        user.address = address
        user.is_active = False

        if commit:
            user.save()
        return user


class RequestNewTokenForm(forms.Form):
    email = forms.EmailField(
        label='Email Address',
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'required': True,
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            if user.is_active:
                raise forms.ValidationError(
                    _("A user account associated with this email address is already active. You cannot request new tokens."))
        else:
            raise forms.ValidationError(
                _("We couldn't find a user with this email address. Please make sure you've entered a valid email address."))
        return email


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=("Old password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
    )
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=("Email"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        }),
    )

    def clean_email(self):
        email = self.cleaned_data['email']

        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError(
                _("No active users were found with this email address. Please enter a valid email address."))
        return email


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
    )
