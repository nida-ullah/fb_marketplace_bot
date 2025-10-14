from django import forms


class BulkAccountUploadForm(forms.Form):
    file = forms.FileField(
        label='Upload Accounts File',
        help_text='Upload a .txt file with email:password per line',
        widget=forms.FileInput(attrs={'accept': '.txt'})
    )
