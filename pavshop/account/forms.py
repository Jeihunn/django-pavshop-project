from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Country, City, Address
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth import get_user_model

User = get_user_model()


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
                "A user with that email already exists.")
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

        if commit:
            user.save()
        return user
