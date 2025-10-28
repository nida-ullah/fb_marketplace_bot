from rest_framework import serializers
from .models import MarketplacePost, PostingJob, ErrorLog
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
    status = serializers.CharField(required=False)
    account = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=FacebookAccount.objects.all()
    )

    class Meta:
        model = MarketplacePost
        fields = [
            'id', 'title', 'description', 'price', 'image',
            'scheduled_time', 'posted', 'status', 'error_message',
            'retry_count', 'account', 'account_email',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'retry_count']

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


class PostingJobSerializer(serializers.ModelSerializer):
    """Serializer for posting job status"""
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = PostingJob
        fields = [
            'id', 'job_id', 'status', 'total_posts', 'completed_posts',
            'failed_posts', 'current_post_id', 'current_post_title',
            'error_message', 'started_at', 'completed_at', 'progress_percentage'
        ]

    def get_progress_percentage(self, obj):
        if obj.total_posts == 0:
            return 0
        return round((obj.completed_posts / obj.total_posts) * 100, 1)


class ErrorLogSerializer(serializers.ModelSerializer):
    """Serializer for error logs"""
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = ErrorLog
        fields = [
            'id', 'post', 'post_title', 'error_type', 'error_message',
            'stack_trace', 'screenshot', 'created_at'
        ]
        read_only_fields = ['created_at']
