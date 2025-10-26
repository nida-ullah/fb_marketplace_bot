from django.db import models
from accounts.models import FacebookAccount


class MarketplacePost(models.Model):

    account = models.ForeignKey(FacebookAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='posts/', blank=True)
    scheduled_time = models.DateTimeField()
    posted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['posted'], name='posted_idx'),
            models.Index(fields=['scheduled_time'], name='scheduled_time_idx'),
            models.Index(fields=['account', 'posted'],
                         name='account_posted_idx'),
            models.Index(fields=['posted', 'scheduled_time'],
                         name='posted_scheduled_idx'),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.account.email}"
