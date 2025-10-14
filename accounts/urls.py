from django.urls import path
from . import views

urlpatterns = [
    path('accounts/bulk-upload/', views.bulk_upload_accounts, name='bulk_upload_accounts'),
]
