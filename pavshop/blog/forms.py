from django import forms
from .models import BlogReview


class BlogReviewAdminForm(forms.ModelForm):
    class Meta:
        model = BlogReview
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")

        if instance:
            if BlogReview.objects.filter(parent=instance).exists():
                self.fields["blog"].disabled = True

    def is_recursive_parent(self, parent, target):
        if parent is None:
            return False
        elif parent == target:
            return True
        else:
            return self.is_recursive_parent(parent.parent, target)

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if parent == self.instance:
            raise forms.ValidationError("A comment cannot be its own parent.")
        elif parent and self.is_recursive_parent(parent, self.instance):
            raise forms.ValidationError(
                "This comment cannot be a parent of its own parent.")
        return parent

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
