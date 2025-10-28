from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os


class CustomUser(AbstractUser):
    """
    Custom User model with approval system.
    Users must be approved by admin before they can login.
    """
    is_approved = models.BooleanField(
        default=False,
        help_text="Designates whether this user has been approved by admin to login."
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time when user was approved"
    )
    approved_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_users',
        help_text="Admin who approved this user"
    )
    rejection_reason = models.TextField(
        blank=True,
        null=True,
        help_text="Reason for rejection (if applicable)"
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def approve(self, approved_by_user):
        """Approve this user"""
        from django.utils import timezone
        self.is_approved = True
        self.approved_at = timezone.now()
        self.approved_by = approved_by_user
        self.rejection_reason = None
        self.save()

    def reject(self, reason=None):
        """Reject/unapprove this user"""
        self.is_approved = False
        self.approved_at = None
        self.approved_by = None
        self.rejection_reason = reason
        self.save()


class FacebookAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='facebook_accounts', null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)  # Store securely in production
    session_cookie = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.email)

    def delete(self, *args, **kwargs):
        # Delete session file when account is deleted
        session_file = f"sessions/{self.email.replace('@', '_').replace('.', '_')}.json"
        if os.path.exists(session_file):
            os.remove(session_file)
            print(f"🗑️ Deleted session file: {session_file}")
        super().delete(*args, **kwargs)
