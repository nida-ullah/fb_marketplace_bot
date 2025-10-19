from django.urls import path
from . import api_views
from .bulk_upload_with_images import BulkUploadWithImagesView

app_name = 'postings_api'

urlpatterns = [
    # Marketplace posts
    path('posts/', api_views.MarketplacePostListCreateView.as_view(), name='post_list'),
    path('posts/<int:pk>/', api_views.MarketplacePostDetailView.as_view(),
         name='post_detail'),
    # Bulk upload (original - CSV with URLs)
    path('posts/bulk-upload/',
         api_views.BulkUploadPostsView.as_view(), name='bulk_upload'),
    # Bulk upload with images (NEW - CSV + ZIP)
    path('posts/bulk-upload-with-images/',
         BulkUploadWithImagesView.as_view(), name='bulk_upload_with_images'),
    # Start posting
    path('posts/start-posting/',
         api_views.StartPostingView.as_view(), name='start_posting'),
]
