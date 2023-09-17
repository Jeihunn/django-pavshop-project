from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings
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

    def is_recursive_parent(self, parent, target): # custom method
        if parent is None:
            return False
        elif parent == target:
            return True
        else:
            return self.is_recursive_parent(parent.parent, target)
        
    def check_max_parent_nesting(self, parent, max_parent_nesting=1): # custom method
        nesting_level = 1
        current_parent = parent

        while current_parent.parent and nesting_level <= max_parent_nesting:
            current_parent = current_parent.parent
            nesting_level += 1

        return nesting_level > max_parent_nesting


    def clean_parent(self):
        parent = self.cleaned_data.get("parent")
        blog = self.cleaned_data.get("blog")

        max_parent_nesting = settings.CUSTOM_VARIABLES["MAX_PARENT_NESTING"]

        if parent:
            if parent.blog != blog:
                raise forms.ValidationError(_("The selected parent review does not belong to the chosen blog."))
            elif parent == self.instance:
                raise forms.ValidationError(_("A comment cannot be its own parent."))
            elif self.is_recursive_parent(parent, self.instance):
                raise forms.ValidationError(_("This comment cannot be a parent of its own parent."))
            elif self.check_max_parent_nesting(parent, max_parent_nesting):
                    raise forms.ValidationError(_("The selected parent comment exceeds the designated maximum sub-comment level. Maximum level: {}").format(max_parent_nesting))

        return parent

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        full_name = cleaned_data.get("full_name")
        email = cleaned_data.get("email")

        if user:
            if full_name or email:
                if full_name:
                    self.add_error("full_name", forms.ValidationError(_("Full name field should be empty when user is specified.")))
                if email:
                    self.add_error("email", forms.ValidationError(_("Email field should be empty when user is specified.")))
        else:
            if not full_name:
                self.add_error("full_name", forms.ValidationError(_("Full name field is required when user is not specified.")))
            if not email:
                self.add_error("email", forms.ValidationError(_("Email field is required when user is not specified.")))
