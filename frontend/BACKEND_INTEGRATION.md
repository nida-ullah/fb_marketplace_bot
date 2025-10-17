# 🔗 Backend Integration Checklist

## Django Backend Setup Required

### 1️⃣ Install Django REST Framework

```bash
cd ../  # Go back to main project folder
source env/bin/activate  # Or: env\Scripts\activate on Windows

pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
```

### 2️⃣ Update Django Settings

**File:** `bot_core/settings.py`

```python
INSTALLED_APPS = [
    # ... existing apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add at top
    # ... existing middleware
]

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}
```

---

### 3️⃣ Create User Model

**File:** `accounts/models.py` (add User model)

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.email
```

**Update settings.py:**
```python
AUTH_USER_MODEL = 'accounts.User'
```

---

### 4️⃣ Create Serializers

**File:** `accounts/serializers.py` (create new file)

```python
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FacebookAccount

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class FacebookAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookAccount
        fields = ['id', 'email', 'password', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}
```

**File:** `postings/serializers.py` (create new file)

```python
from rest_framework import serializers
from .models import MarketplacePost
from accounts.serializers import FacebookAccountSerializer

class MarketplacePostSerializer(serializers.ModelSerializer):
    account_details = FacebookAccountSerializer(source='account', read_only=True)
    
    class Meta:
        model = MarketplacePost
        fields = [
            'id', 'account', 'account_details', 'title', 
            'description', 'price', 'image', 'scheduled_time', 
            'posted', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
```

---

### 5️⃣ Create API Views

**File:** `accounts/api_views.py` (create new file)

```python
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import FacebookAccount
from .serializers import UserSerializer, RegisterSerializer, FacebookAccountSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(email=email, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    
    return Response(
        {'message': 'Invalid credentials'}, 
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    return Response(UserSerializer(request.user).data)

class FacebookAccountViewSet(viewsets.ModelViewSet):
    queryset = FacebookAccount.objects.all()
    serializer_class = FacebookAccountSerializer
    permission_classes = [IsAuthenticated]
```

**File:** `postings/api_views.py` (create new file)

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MarketplacePost
from .serializers import MarketplacePostSerializer

class MarketplacePostViewSet(viewsets.ModelViewSet):
    queryset = MarketplacePost.objects.all()
    serializer_class = MarketplacePostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MarketplacePost.objects.all().order_by('-scheduled_time')
```

---

### 6️⃣ Create Stats View

**File:** `automation/api_views.py` (create new file)

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import FacebookAccount
from postings.models import MarketplacePost
from django.utils import timezone
from datetime import timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    total_accounts = FacebookAccount.objects.count()
    total_posts = MarketplacePost.objects.count()
    pending_posts = MarketplacePost.objects.filter(posted=False).count()
    
    # Posts today
    today = timezone.now().date()
    posted_today = MarketplacePost.objects.filter(
        posted=True,
        scheduled_time__date=today
    ).count()
    
    # Success rate
    total_attempted = MarketplacePost.objects.filter(posted=True).count()
    success_rate = (total_attempted / total_posts * 100) if total_posts > 0 else 0
    
    return Response({
        'total_accounts': total_accounts,
        'active_accounts': total_accounts,  # You can add logic for active check
        'total_posts': total_posts,
        'pending_posts': pending_posts,
        'posted_today': posted_today,
        'success_rate': round(success_rate, 1)
    })
```

---

### 7️⃣ Update URLs

**File:** `bot_core/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.api_urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/posts/', include('postings.urls')),
    path('api/stats/', include('automation.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**File:** `accounts/api_urls.py` (create new file)

```python
from django.urls import path
from .api_views import login_view, signup_view, profile_view

urlpatterns = [
    path('login/', login_view, name='api_login'),
    path('signup/', signup_view, name='api_signup'),
    path('profile/', profile_view, name='api_profile'),
]
```

**File:** `accounts/urls.py`

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import FacebookAccountViewSet

router = DefaultRouter()
router.register('', FacebookAccountViewSet, basename='facebook-account')

urlpatterns = [
    path('', include(router.urls)),
]
```

**File:** `postings/urls.py`

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import MarketplacePostViewSet

router = DefaultRouter()
router.register('', MarketplacePostViewSet, basename='marketplace-post')

urlpatterns = [
    path('', include(router.urls)),
]
```

**File:** `automation/api_urls.py` (create new file)

```python
from django.urls import path
from .api_views import dashboard_stats

urlpatterns = [
    path('dashboard/', dashboard_stats, name='dashboard_stats'),
]
```

---

### 8️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

### 9️⃣ Test Backend API

**Start Django server:**
```bash
python manage.py runserver
```

**Test with curl or Postman:**

```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "Test User", "password": "password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Get Profile (with token)
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Dashboard Stats
curl -X GET http://localhost:8000/api/stats/dashboard/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

### 🔟 Connect Frontend

**Create `.env.local` in frontend:**
```bash
cd frontend
cp .env.local.example .env.local
```

**Content of `.env.local`:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

**Start frontend:**
```bash
npm run dev
```

---

## ✅ Testing Checklist

### Backend Tests
- [ ] Django server starts without errors
- [ ] Signup endpoint returns token
- [ ] Login endpoint returns token
- [ ] Profile endpoint requires authentication
- [ ] Dashboard stats endpoint returns data
- [ ] CORS allows requests from localhost:3000

### Frontend Tests
- [ ] Frontend server starts (port 3000)
- [ ] Can navigate to /login
- [ ] Can sign up new user
- [ ] Receives token after signup
- [ ] Redirected to dashboard after login
- [ ] Dashboard loads stats
- [ ] Logout clears token
- [ ] Protected routes redirect to login

### Integration Tests
- [ ] Signup → Dashboard flow works
- [ ] Login → Dashboard flow works
- [ ] Logout → Login flow works
- [ ] Token persists on page refresh
- [ ] API errors show in frontend
- [ ] Network tab shows correct requests

---

## 🐛 Troubleshooting

### CORS Errors
```python
# In settings.py, add:
CORS_ALLOW_ALL_ORIGINS = True  # For development only!
```

### 401 Unauthorized
- Check token is being sent in headers
- Check token hasn't expired
- Check JWT settings in Django

### Module Not Found
```bash
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
```

### Port Already in Use
```bash
# Django
fuser -k 8000/tcp

# Next.js
npx kill-port 3000
```

---

## 📚 Documentation Links

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Django CORS Headers](https://github.com/adamchainz/django-cors-headers)

---

## 🎉 Success!

When everything works, you should see:
1. ✅ Django backend running on port 8000
2. ✅ Next.js frontend running on port 3000
3. ✅ User can sign up and login
4. ✅ Dashboard shows real data from database
5. ✅ All API calls successful (check Network tab)

---

**Next:** Build the remaining dashboard pages (Accounts, Posts, Bulk Upload, Analytics, Settings)
