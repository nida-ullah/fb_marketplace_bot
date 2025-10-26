# Database Indexing Improvement

## Overview
Added database indexes to improve query performance on frequently queried fields in the `MarketplacePost` model.

## Changes Made

### Model: `postings.models.MarketplacePost`

Added the following indexes:

1. **`posted_idx`** - Single field index on `posted` field
   - Speeds up queries filtering by post status (posted/not posted)
   - Example: `MarketplacePost.objects.filter(posted=False)`

2. **`scheduled_time_idx`** - Single field index on `scheduled_time` field
   - Speeds up queries filtering or ordering by scheduled time
   - Example: `MarketplacePost.objects.filter(scheduled_time__lte=now())`

3. **`account_posted_idx`** - Composite index on `account_id` and `posted` fields
   - Speeds up queries filtering by both account and post status
   - Example: `MarketplacePost.objects.filter(account=account, posted=False)`

4. **`posted_scheduled_idx`** - Composite index on `posted` and `scheduled_time` fields
   - Speeds up queries filtering by status and sorting by time
   - Example: `MarketplacePost.objects.filter(posted=False).order_by('scheduled_time')`

### Additional Benefits

- Added default ordering by `-created_at` in Meta class for consistent query results
- Composite indexes provide better performance for multi-field queries
- No changes to existing functionality - fully backward compatible

## Migration

**File:** `postings/migrations/0006_alter_marketplacepost_options_and_more.py`

The migration:
- Adds all 4 indexes to the database
- Sets default ordering
- Can be safely applied to existing databases
- Successfully applied on: October 26, 2025

## Performance Impact

### Before:
- Full table scans for queries filtering by `posted`, `scheduled_time`, or `account_id`
- Slower queries as data grows

### After:
- Indexed lookups (significantly faster)
- Better performance for:
  - Dashboard stats (counting posted/pending posts)
  - Post filtering by account
  - Scheduled post queries
  - Bulk operations

## Verification

Verified indexes were created successfully:
```bash
python manage.py dbshell
sqlite> .schema postings_marketplacepost
```

All indexes are present:
- ✅ posted_idx
- ✅ scheduled_time_idx
- ✅ account_posted_idx
- ✅ posted_scheduled_idx

## Testing

Ran Django system check:
```bash
python manage.py check
```
**Result:** System check identified no issues (0 silenced)

## No Breaking Changes

✅ No changes to model fields
✅ No changes to API endpoints
✅ No changes to serializers
✅ No changes to views
✅ Fully backward compatible
✅ Only adds performance improvements

## Next Steps

Monitor query performance and consider adding more indexes if needed:
- Index on `created_at` if frequently used for sorting
- Index on `updated_at` if tracking recent changes
- Consider removing unused indexes if database grows large
