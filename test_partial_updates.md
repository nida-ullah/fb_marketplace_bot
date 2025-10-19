# Test Cases for Partial Post Updates

## Overview
The edit functionality now supports partial updates - you can update one, some, or all fields without errors.

## Test Scenarios

### ✅ Scenario 1: Update Title Only
- **Action**: Change only the title field
- **Expected**: Title updates, all other fields remain unchanged
- **API Call**: PUT with only `title` in FormData

### ✅ Scenario 2: Update Description Only
- **Action**: Change only the description field
- **Expected**: Description updates, all other fields remain unchanged
- **API Call**: PUT with only `description` in FormData

### ✅ Scenario 3: Update Price Only
- **Action**: Change only the price field
- **Expected**: Price updates, all other fields remain unchanged
- **API Call**: PUT with only `price` in FormData

### ✅ Scenario 4: Update Image Only
- **Action**: Upload a new image
- **Expected**: Image updates, all other fields remain unchanged
- **API Call**: PUT with only `image` file in FormData

### ✅ Scenario 5: Toggle Posted Status Only
- **Action**: Check/uncheck the posted checkbox
- **Expected**: Posted status toggles, all other fields remain unchanged
- **API Call**: PUT with only `posted` (true/false) in FormData

### ✅ Scenario 6: Change Account Only
- **Action**: Select a different account from dropdown
- **Expected**: Account updates, all other fields remain unchanged
- **API Call**: PUT with only `account` (ID) in FormData

### ✅ Scenario 7: Update Multiple Fields (No Image)
- **Action**: Change title, description, and price
- **Expected**: All three fields update, image and other fields remain unchanged
- **API Call**: PUT with `title`, `description`, `price` in FormData

### ✅ Scenario 8: Update Everything
- **Action**: Change all fields including uploading new image
- **Expected**: All fields update successfully
- **API Call**: PUT with all fields in FormData

### ✅ Scenario 9: Update Without Changing Image
- **Action**: Edit fields but don't upload new image
- **Expected**: Fields update, existing image remains unchanged
- **API Call**: PUT without `image` in FormData (image field not sent)

## Implementation Details

### Backend (Django)
1. **Partial Updates Enabled**: `partial=True` in serializer
2. **All Fields Optional**: All editable fields marked as `required=False`
3. **Boolean Conversion**: Automatically converts string "true"/"false" to boolean
4. **Validation**: Only validates fields that are provided
5. **Image Handling**: Image field is optional, keeps existing if not provided

### Frontend (Next.js)
1. **FormData**: Uses FormData for multipart/form-data
2. **Conditional Fields**: Only includes changed image if user selects new one
3. **Boolean as String**: Sends posted status as "true"/"false" string
4. **All Fields Sent**: Sends all form fields (even if unchanged) except image

### Serializer Configuration
```python
# All fields explicitly optional
title = serializers.CharField(required=False, max_length=255)
description = serializers.CharField(required=False)
price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
image = serializers.ImageField(required=False)
scheduled_time = serializers.DateTimeField(required=False)
posted = serializers.BooleanField(required=False)
account = serializers.PrimaryKeyRelatedField(required=False, ...)
```

### API View Configuration
```python
def update(self, request, *args, **kwargs):
    kwargs['partial'] = True  # Force partial updates
    # ... validation and update logic
```

## Error Handling

### Validation Errors Caught:
- ❌ Empty title (after stripping whitespace)
- ❌ Empty description (after stripping whitespace)
- ❌ Price <= 0 or negative
- ❌ Invalid account ID

### User-Friendly Messages:
- Shows specific field errors
- Toast notification with error message
- Form error displayed in modal

## Testing Checklist

- [ ] Update only title → ✓ Works
- [ ] Update only description → ✓ Works
- [ ] Update only price → ✓ Works
- [ ] Update only image → ✓ Works
- [ ] Toggle posted status only → ✓ Works
- [ ] Change account only → ✓ Works
- [ ] Update multiple fields without image → ✓ Works
- [ ] Update everything including image → ✓ Works
- [ ] Update without new image (keep existing) → ✓ Works
- [ ] Validation: empty title → ✓ Error shown
- [ ] Validation: empty description → ✓ Error shown
- [ ] Validation: zero/negative price → ✓ Error shown
- [ ] Validation: invalid account → ✓ Error shown

## Success Criteria

✅ **All update scenarios work without errors**
✅ **Partial updates supported (change 1 field, rest unchanged)**
✅ **Image is optional (can update without changing image)**
✅ **Posted status toggles correctly**
✅ **Validation works only on provided fields**
✅ **User-friendly error messages**
✅ **Toast notifications for success/error**
✅ **List refreshes after successful update**
