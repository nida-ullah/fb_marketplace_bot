from django.urls import path
from . import api_views

app_name = 'postings_api'

urlpatterns = [
    # Marketplace posts
    path('posts/', api_views.MarketplacePostListCreateView.as_view(), name='post_list'),
    path('posts/<int:pk>/', api_views.MarketplacePostDetailView.as_view(),
         name='post_detail'),
    # Bulk upload
    path('posts/bulk-upload/',
         api_views.BulkUploadPostsView.as_view(), name='bulk_upload'),
]
