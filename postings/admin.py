from django.contrib import admin
from .models import MarketplacePost

# admin.site.register(MarketplacePost)


@admin.register(MarketplacePost)
class MarketplacePostAdmin(admin.ModelAdmin):
    list_display = ['title', 'account',
                    'scheduled_time', 'posted']
    list_filter = ['posted']
