from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer, FacebookAccountSerializer
from .models import FacebookAccount
from postings.models import MarketplacePost
from automation.post_to_facebook import save_session
from threading import Thread
import os


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return JWT tokens"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Allow login with email or username
    if email and not username:
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })

    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    """Get current user profile"""
    return Response(UserSerializer(request.user).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics"""
    total_accounts = FacebookAccount.objects.count()
    total_posts = MarketplacePost.objects.count()
    pending_posts = MarketplacePost.objects.filter(posted=False).count()
    posted_today = MarketplacePost.objects.filter(posted=True).count()

    # Calculate success rate
    posted_posts = MarketplacePost.objects.filter(posted=True).count()
    success_rate = (posted_posts / total_posts * 100) if total_posts > 0 else 0

    return Response({
        'total_accounts': total_accounts,
        'total_posts': total_posts,
        'pending_posts': pending_posts,
        'posted_today': posted_today,
        'success_rate': round(success_rate, 1)
    })


class FacebookAccountListCreateView(generics.ListCreateAPIView):
    """List all Facebook accounts or create a new one"""
    queryset = FacebookAccount.objects.all()
    serializer_class = FacebookAccountSerializer
    permission_classes = [IsAuthenticated]


class FacebookAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a Facebook account"""
    queryset = FacebookAccount.objects.all()
    serializer_class = FacebookAccountSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """Override delete to also remove session file"""
        account = self.get_object()

        # Delete session file if exists
        session_file = f"sessions/{account.email.replace('@', '_').replace('.', '_')}.json"
        if os.path.exists(session_file):
            os.remove(session_file)

        return super().delete(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_facebook_account_with_login(request):
    """
    Add a new Facebook account and automatically open browser for login.
    If CAPTCHA appears, user can solve it manually.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if account already exists
    if FacebookAccount.objects.filter(email=email).exists():
        return Response(
            {'error': 'Account with this email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create account in database
    account = FacebookAccount.objects.create(
        email=email,
        password=password
    )

    # Start browser automation in background thread
    def automated_login():
        try:
            print(f"\n🌐 Opening browser for {email}...")
            success = save_session(email, password)
            if success:
                print(f"✅ Session saved successfully for {email}")
            else:
                print(f"❌ Login failed for {email}")
        except Exception as e:
            print(f"❌ Error during automated login: {e}")

    # Start the login process in a background thread
    thread = Thread(target=automated_login, daemon=True)
    thread.start()

    # Return response immediately with account data
    serializer = FacebookAccountSerializer(account)
    return Response({
        'message': 'Account created successfully. Browser opening for login...',
        'account': serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_upload_accounts_with_login(request):
    """
    Bulk upload Facebook accounts from a text file.
    Format: email:password (one per line)
    Browser will open for each account to save session.
    """
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    file = request.FILES['file']

    # Validate file type
    if not file.name.endswith('.txt'):
        return Response(
            {'error': 'Only .txt files are allowed'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Read and parse file
        content = file.read().decode('utf-8')
        lines = content.strip().split('\n')

        accounts_created = []
        accounts_skipped = []
        accounts_failed = []

        for line in lines:
            line = line.strip()

            # Skip empty lines or comments
            if not line or line.startswith('#') or ':' not in line:
                continue

            try:
                # Split email and password
                parts = line.split(':', 1)
                if len(parts) != 2:
                    accounts_failed.append({
                        'line': line,
                        'error': 'Invalid format (use email:password)'
                    })
                    continue

                email = parts[0].strip()
                password = parts[1].strip()

                # Validate email and password
                if not email or not password:
                    accounts_failed.append({
                        'line': line,
                        'error': 'Email or password is empty'
                    })
                    continue

                # Check if account already exists
                if FacebookAccount.objects.filter(email=email).exists():
                    accounts_skipped.append(email)
                    continue

                # Create account in database
                account = FacebookAccount.objects.create(
                    email=email,
                    password=password
                )
                accounts_created.append(email)

            except Exception as e:
                accounts_failed.append({
                    'line': line,
                    'error': str(e)
                })

        # Start browser automation for all new accounts in background
        if accounts_created:
            def process_bulk_sessions():
                for email in accounts_created:
                    try:
                        account = FacebookAccount.objects.get(email=email)
                        print(f"\n🌐 Opening browser for {email}...")
                        success = save_session(email, account.password)
                        if success:
                            print(f"✅ Session saved for {email}")
                        else:
                            print(f"❌ Login failed for {email}")
                    except Exception as e:
                        print(f"❌ Error processing {email}: {e}")

            thread = Thread(target=process_bulk_sessions, daemon=True)
            thread.start()

        return Response({
            'message': f'Bulk upload completed. Processing {len(accounts_created)} accounts...',
            'summary': {
                'created': len(accounts_created),
                'skipped': len(accounts_skipped),
                'failed': len(accounts_failed)
            },
            'details': {
                'created_accounts': accounts_created,
                'skipped_accounts': accounts_skipped,
                'failed_accounts': accounts_failed
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'error': f'Failed to process file: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_account_session(request, pk):
    """
    Update session for an existing account by opening browser for re-login.
    Used when session expires or doesn't exist.
    """
    try:
        account = FacebookAccount.objects.get(pk=pk)

        # Start browser automation in background thread
        def update_session():
            try:
                print(f"\n🔄 Update Session requested for: {account.email}")
                print(f"🌐 Opening browser for re-login...")
                success = save_session(account.email, account.password)
                if success:
                    print(
                        f"✅ Session updated successfully for {account.email}")
                else:
                    print(f"❌ Session update failed for {account.email}")
            except Exception as e:
                print(f"❌ Error updating session: {e}")

        thread = Thread(target=update_session, daemon=True)
        thread.start()

        # Return response immediately
        serializer = FacebookAccountSerializer(account)
        return Response({
            'message': f'Browser opening for {account.email}. Please complete login if CAPTCHA appears.',
            'account': serializer.data
        }, status=status.HTTP_200_OK)

    except FacebookAccount.DoesNotExist:
        return Response(
            {'error': 'Account not found'},
            status=status.HTTP_404_NOT_FOUND
        )
