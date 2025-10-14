from django.db import models
import os


class FacebookAccount(models.Model):
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
