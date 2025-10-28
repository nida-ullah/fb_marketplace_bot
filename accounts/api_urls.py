from django.urls import path
from . import api_views
from postings import realtime_views

app_name = 'accounts_api'

urlpatterns = [
    # Authentication
    path('auth/register/', api_views.register, name='register'),
    path('auth/login/', api_views.login, name='login'),
    path('auth/user/', api_views.get_user, name='get_user'),

    # Dashboard stats
    path('stats/dashboard/', api_views.dashboard_stats, name='dashboard_stats'),

    # Facebook accounts
    path('accounts/', api_views.FacebookAccountListCreateView.as_view(),
         name='account_list'),
    path('accounts/add-with-login/', api_views.add_facebook_account_with_login,
         name='add_account_with_login'),
    path('accounts/bulk-upload/', api_views.bulk_upload_accounts_with_login,
         name='bulk_upload_accounts'),
    path('accounts/<int:pk>/update-session/', api_views.update_account_session,
         name='update_account_session'),
    path('accounts/<int:pk>/',
         api_views.FacebookAccountDetailView.as_view(), name='account_detail'),

    # Health checks
    path('accounts/health-check/',
         realtime_views.health_check_accounts, name='health_check_accounts'),
    path('accounts/<int:account_id>/validate-session/',
         realtime_views.validate_account_session, name='validate_session'),
]
