from django.db import models
from accounts.models import FacebookAccount


class MarketplacePost(models.Model):

    account = models.ForeignKey(FacebookAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='posts/')
    scheduled_time = models.DateTimeField()
    posted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.account.email}"
