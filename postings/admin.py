from django.contrib import admin
from .models import MarketplacePost
from django.urls import reverse

# admin.site.register(MarketplacePost)


@admin.register(MarketplacePost)
class MarketplacePostAdmin(admin.ModelAdmin):
    list_display = ['title', 'account', 'price', 'posted']
    list_filter = ['posted', 'account']
    search_fields = ['title', 'description', 'account__email']
    exclude = ['scheduled_time']  # Hide scheduled_time from admin forms

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['bulk_upload_url'] = reverse('bulk_upload_posts')
        return super().changelist_view(request, extra_context=extra_context)
