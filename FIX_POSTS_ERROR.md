# Fix for Posts Page 500 Error

## Problem
The posts API endpoint was returning a 500 error because the `MarketplacePost` model didn't have a `created_at` field, but the API view was trying to order by it.

## Solution Applied

### 1. Updated Model (postings/models.py)
Added `created_at` and `updated_at` timestamp fields:
```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

### 2. Updated Serializer (postings/serializers.py)
Added the new fields to the serializer output.

### 3. Created Migration
Created migration file: `0004_marketplacepost_created_at_and_more.py`

## Steps to Fix

Run these commands in your terminal:

```bash
# Navigate to project directory
cd "c:/Users/NidaUllah/OneDrive - Higher Education Commission/Documents/Development/fb_marketplace_bot"

# Apply the migration
python manage.py migrate

# Restart Django server
python manage.py runserver
```

After running these commands, refresh your frontend and the posts page should work!

## What This Fixes
- ✅ Posts API endpoint will now work without 500 error
- ✅ Posts will be ordered by creation date (newest first)
- ✅ You can track when posts were created and last updated
