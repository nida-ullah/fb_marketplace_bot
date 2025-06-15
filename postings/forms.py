from django import forms
from .models import MarketplacePost


class MarketplacePostForm(forms.ModelForm):
    class Meta:
        model = MarketplacePost
        fields = ['account', 'title', 'description',
                  'price', 'image', 'scheduled_time']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
