from rest_framework import serializers
from .models import MarketplacePost
from accounts.models import FacebookAccount


class MarketplacePostSerializer(serializers.ModelSerializer):
    account_email = serializers.EmailField(
        source='account.email', read_only=True)

    # Make all fields optional for updates (partial updates)
    title = serializers.CharField(required=False, max_length=255)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(
        required=False, max_digits=10, decimal_places=2)
    image = serializers.ImageField(required=False)
    scheduled_time = serializers.DateTimeField(required=False)
    posted = serializers.BooleanField(required=False)
    account = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=FacebookAccount.objects.all()
    )

    class Meta:
        model = MarketplacePost
        fields = [
            'id', 'title', 'description', 'price', 'image',
            'scheduled_time', 'posted', 'account', 'account_email',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_price(self, value):
        """Validate that price is positive"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_title(self, value):
        """Validate that title is not empty if provided"""
        if value is not None and not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value

    def validate_description(self, value):
        """Validate that description is not empty if provided"""
        if value is not None and not value.strip():
            raise serializers.ValidationError("Description cannot be empty")
        return value
