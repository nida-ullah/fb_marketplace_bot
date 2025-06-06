from django.db import models


class FacebookAccount(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)  # Store securely in production
    session_cookie = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.email)
