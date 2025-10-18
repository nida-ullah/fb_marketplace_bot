# Image URL Feature

## Overview
The Create Post feature now supports two ways to add product images:
1. **Upload File**: Select an image file from your computer (PNG, JPG, GIF up to 5MB)
2. **Image URL**: Paste a URL of an image from the web

## Features

### Frontend Changes (`CreatePostModal.tsx`)

#### 1. Toggle Interface
- Two-button toggle to switch between "Upload File" and "Image URL" modes
- Active mode is highlighted in blue
- Switching modes clears the previous image selection

#### 2. File Upload Mode
- Drag & drop or click to upload
- Image validation (file type and size)
- Live preview of uploaded image
- Remove button to clear selection

#### 3. Image URL Mode
- Text input field for pasting image URLs
- Live preview when valid URL is entered
- Error handling for invalid/failed images
- Clear button to reset the URL

#### 4. State Management
```typescript
const [imageInputType, setImageInputType] = useState<"file" | "url">("file");
const [image, setImage] = useState<File | null>(null);
const [imageUrl, setImageUrl] = useState<string>("");
const [imagePreview, setImagePreview] = useState<string>("");
```

#### 5. Validation
- Ensures either file OR URL is provided (not both)
- Shows appropriate error messages
- Validates image accessibility before submission

### Backend Changes (`api_views.py`)

#### 1. Image URL Processing
The `MarketplacePostListCreateView.create()` method now:
- Checks if `image_url` is provided in the request
- Downloads the image from the URL using `requests.get()`
- Validates HTTP response status (200 OK)
- Extracts or generates filename from URL
- Creates a Django `ContentFile` from the downloaded content
- Saves the image to the model's ImageField

#### 2. Error Handling
- HTTP errors (non-200 responses)
- Network/timeout errors
- Invalid URLs
- All errors return appropriate error responses with clear messages

#### 3. Code Flow
```python
if image_url and not request.data.get('image'):
    # Download image
    response = requests.get(image_url, timeout=10)
    
    # Extract filename
    filename = os.path.basename(urlparse(image_url).path)
    
    # Save to database
    instance = serializer.save()
    image_content = ContentFile(response.content)
    instance.image.save(filename, image_content, save=True)
```

## How to Use

### For Users

1. **Open Create Post Modal**
   - Click "Create Post" button on the Posts page

2. **Choose Image Input Method**
   - Click "Upload File" button for local images
   - Click "Image URL" button for web images

3. **Upload File Method**
   - Click "Select Image" or drag file into the upload area
   - Preview appears automatically
   - Click "Remove Image" to clear

4. **Image URL Method**
   - Paste the complete image URL (e.g., `https://example.com/image.jpg`)
   - Preview appears automatically if URL is valid
   - Click "Clear URL" to reset

5. **Submit**
   - Fill in other required fields (accounts, title, description, price)
   - Click "Create Post" to submit

### Example URLs for Testing
```
https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800
https://picsum.photos/800/600
https://via.placeholder.com/600x400
```

## Technical Details

### API Request Format

#### With File Upload
```javascript
const formData = new FormData();
formData.append('title', 'Product Title');
formData.append('description', 'Description');
formData.append('price', '99.99');
formData.append('account', '1');
formData.append('image', fileObject);
```

#### With Image URL
```javascript
const formData = new FormData();
formData.append('title', 'Product Title');
formData.append('description', 'Description');
formData.append('price', '99.99');
formData.append('account', '1');
formData.append('image_url', 'https://example.com/image.jpg');
```

### Backend Dependencies
```python
import requests  # For downloading images from URLs
from django.core.files.base import ContentFile  # For creating file objects
from urllib.parse import urlparse  # For parsing URLs
import os  # For filename extraction
```

### Error Messages

#### Frontend
- "Please upload an image or provide an image URL"
- "Please provide either an uploaded image OR an image URL, not both"
- "Invalid image URL or image failed to load"

#### Backend
- "Failed to download image from URL (HTTP {status_code})"
- "Error downloading image: {exception_message}"

## Benefits

1. **Flexibility**: Users can choose the most convenient method
2. **Efficiency**: No need to download images locally first
3. **Bulk Operations**: Easier to create multiple posts with images from the web
4. **Storage**: Centralizes image storage in your media folder
5. **Consistency**: All images are processed the same way regardless of source

## Security Considerations

1. **Timeout**: 10-second timeout prevents hanging on slow URLs
2. **Validation**: HTTP status code checking ensures valid responses
3. **File Type**: Django's ImageField validates uploaded content
4. **Size Limit**: Frontend enforces 5MB limit for uploads
5. **Error Handling**: Graceful failures with clear error messages

## Future Enhancements

Potential improvements:
- [ ] Image size validation for URL downloads
- [ ] Support for multiple image formats/conversions
- [ ] Image optimization/compression before saving
- [ ] Caching of downloaded images
- [ ] Support for bulk URL imports
- [ ] Preview thumbnails for URL validation
- [ ] Image hosting service integrations
