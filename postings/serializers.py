from rest_framework import serializers
from .models import MarketplacePost
from accounts.models import FacebookAccount


class MarketplacePostSerializer(serializers.ModelSerializer):
    account_email = serializers.EmailField(
        source='account.email', read_only=True)

    class Meta:
        model = MarketplacePost
        fields = [
            'id', 'title', 'description', 'price', 'image',
            'scheduled_time', 'posted', 'account', 'account_email',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['posted', 'created_at', 'updated_at']
