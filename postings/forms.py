from django import forms
from accounts.models import FacebookAccount


class MarketplacePostForm(forms.Form):
    """Form for creating posts for multiple accounts"""
    accounts = forms.ModelMultipleChoiceField(
        queryset=FacebookAccount.objects.all(),
        label='Facebook Accounts',
        help_text='Select one or more accounts (Ctrl/Cmd + Click for multiple). Post will be created for each selected account.',
        required=True,
        widget=forms.SelectMultiple(
            attrs={'class': 'form-select', 'size': '5'})
    )
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'step': '0.01'})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text='Upload an image file (optional)'
    )
    image_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com/image.jpg'
        }),
        help_text='Or provide an image URL (optional)'
    )

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')

        # Both image and image_url are optional, but if both provided, prioritize uploaded file
        if image and image_url:
            self.add_error(
                'image_url', 'Please provide either an uploaded image OR an image URL, not both.')

        return cleaned_data


class BulkPostUploadForm(forms.Form):
    """Form for bulk uploading posts via CSV"""
    accounts = forms.ModelMultipleChoiceField(
        queryset=FacebookAccount.objects.all(),
        label='Facebook Accounts',
        help_text='Select one or more accounts to distribute posts across (hold Ctrl/Cmd to select multiple)',
        required=True,
        widget=forms.SelectMultiple(
            attrs={'class': 'form-select', 'size': '5'})
    )
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: title, description, price, image_url (optional)',
        widget=forms.FileInput(attrs={'accept': '.csv'})
    )
