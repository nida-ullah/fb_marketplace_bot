"""
Cache utility functions for managing cache invalidation
"""
from django.core.cache import cache


def invalidate_dashboard_cache():
    """Invalidate dashboard statistics cache"""
    cache.delete('dashboard_stats')


def invalidate_posts_cache():
    """Invalidate posts list cache"""
    cache.delete('posts_list')


def invalidate_accounts_cache():
    """Invalidate accounts list cache"""
    cache.delete('accounts_list')


def invalidate_all_caches():
    """Invalidate all application caches"""
    invalidate_dashboard_cache()
    invalidate_posts_cache()
    invalidate_accounts_cache()
