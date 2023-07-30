from django import forms
from .models import ProductVersionReview


class ProductVersionReviewAdminForm(forms.ModelForm):
    class Meta:
        model = ProductVersionReview
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        full_name = cleaned_data.get('full_name')
        email = cleaned_data.get('email')

        if user:
            if full_name or email:
                if full_name:
                    self.add_error('full_name', forms.ValidationError(
                        "Full name field should be empty when user is specified.", code='invalid_full_name'))
                if email:
                    self.add_error('email', forms.ValidationError(
                        "Email field should be empty when user is specified.", code='invalid_email'))
        else:
            if not full_name:
                self.add_error('full_name', forms.ValidationError(
                    "Full name field is required when user is not specified.", code='required_full_name'))
            if not email:
                self.add_error('email', forms.ValidationError(
                    "Email field is required when user is not specified.", code='required_email'))


class ProductVersionReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.set_required_fields()

    class Meta:
        model = ProductVersionReview
        fields = (
            "full_name",
            "email",
            "comment",
        )

    def set_required_fields(self):
        if self.user and self.user.is_authenticated:
            self.fields['full_name'].required = False
            self.fields['email'].required = False
        else:
            self.fields['full_name'].required = True
            self.fields['email'].required = True
