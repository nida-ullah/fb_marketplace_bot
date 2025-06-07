from django import forms
from .models import MarketplacePost


class MarketplacePostForm(forms.ModelForm):
    class Meta:
        model = MarketplacePost
        fields = [
            'account', 'title', 'description', 'price', 'image',
            'scheduled_time', 'category', 'condition', 'availability',
            'public_meetup', 'door_pickup', 'door_dropoff',
            'brand', 'color', 'sku', 'tags'
        ]
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas (optional)'}),
            'sku': forms.TextInput(attrs={'placeholder': 'Enter SKU (optional)'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Enter brand name (optional)'}),
            'color': forms.TextInput(attrs={'placeholder': 'Enter color (optional)'}),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'help_text': 'Facebook will try to auto-detect the category based on your title and description. You can override this by selecting a category here.'
            }),
            'availability': forms.RadioSelect(),
            'public_meetup': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'door_pickup': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'door_dropoff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'category': 'Facebook will try to auto-detect the category based on your title and description. You can override this by selecting a category here.',
            'sku': 'Stock Keeping Unit - Optional identifier for your product',
            'tags': 'Comma-separated tags for better searchability',
            'availability': 'Choose how you want to list your item',
            'public_meetup': 'Allow buyers to meet in a public location',
            'door_pickup': 'Allow buyers to pick up from your location',
            'door_dropoff': 'Offer to deliver to buyer\'s location',
            'brand': 'Enter the brand name of your product (optional)',
            'color': 'Enter the color of your product (optional)',
        }
