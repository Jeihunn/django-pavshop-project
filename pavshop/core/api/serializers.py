from rest_framework import serializers
from core.models import Newsletter


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ("email", "subscription_status")
        
        read_only_fields = ("subscription_status",)