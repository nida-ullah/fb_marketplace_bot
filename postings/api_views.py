from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import MarketplacePost
from .serializers import MarketplacePostSerializer
from accounts.models import FacebookAccount
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse
import os
import csv
import io
from django.utils import timezone


class MarketplacePostListCreateView(generics.ListCreateAPIView):
    """List all marketplace posts or create a new one"""
    queryset = MarketplacePost.objects.all()
    serializer_class = MarketplacePostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Optionally filter by status"""
        queryset = MarketplacePost.objects.all().order_by('-created_at')
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def create(self, request, *args, **kwargs):
        """Handle post creation with optional image URL"""
        # Check if image_url is provided
        image_url = request.data.get('image_url')

        if image_url and not request.data.get('image'):
            # Download image from URL
            try:
                response = requests.get(image_url, timeout=10, stream=True)
                if response.status_code == 200:
                    # Get filename from URL or generate one
                    parsed_url = urlparse(image_url)
                    filename = os.path.basename(parsed_url.path)
                    if not filename or '.' not in filename:
                        # Generate filename from title
                        title = request.data.get('title', 'image')
                        filename = f"{title[:30].replace(' ', '_')}.jpg"

                    # Create serializer with the data
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)

                    # Save the instance and then add the image
                    instance = serializer.save()

                    # Save the downloaded image to the instance
                    image_content = ContentFile(response.content)
                    instance.image.save(filename, image_content, save=True)

                    # Return the updated instance
                    output_serializer = self.get_serializer(instance)
                    headers = self.get_success_headers(output_serializer.data)
                    return Response(
                        output_serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers
                    )
                else:
                    return Response(
                        {'error': f'Failed to download image from URL (HTTP {response.status_code})'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except requests.exceptions.RequestException as e:
                return Response(
                    {'error': f'Error downloading image: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().create(request, *args, **kwargs)


class MarketplacePostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a marketplace post"""
    queryset = MarketplacePost.objects.all()
    serializer_class = MarketplacePostSerializer
    permission_classes = [IsAuthenticated]


class BulkUploadPostsView(APIView):
    """Handle bulk upload of posts via CSV file"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Process CSV file and create posts for selected accounts"""
        csv_file = request.FILES.get('csv_file')
        account_ids = request.data.getlist(
            'accounts[]') or request.data.getlist('accounts')

        # Validation
        if not csv_file:
            return Response(
                {'error': 'CSV file is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not csv_file.name.endswith('.csv'):
            return Response(
                {'error': 'Please upload a CSV file'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not account_ids:
            return Response(
                {'error': 'Please select at least one account'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get selected accounts
        try:
            accounts = FacebookAccount.objects.filter(id__in=account_ids)
            if not accounts.exists():
                return Response(
                    {'error': 'No valid accounts found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': f'Error fetching accounts: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Parse CSV
        try:
            decoded_file = csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(decoded_file))

            success_count = 0
            error_count = 0
            errors = []
            posts_data = []

            # First pass: Validate and collect all post data
            for row_num, row in enumerate(csv_reader, start=2):
                try:
                    # Extract data from CSV
                    title = row.get('title', '').strip()
                    description = row.get('description', '').strip()
                    price = row.get('price', '').strip()
                    image_url = row.get('image_url', '').strip()

                    # Validate required fields
                    if not all([title, description, price]):
                        errors.append({
                            'row': row_num,
                            'error': 'Missing required fields (title, description, or price)'
                        })
                        error_count += 1
                        continue

                    # Validate price
                    try:
                        price_decimal = float(price)
                        if price_decimal < 0:
                            raise ValueError("Price cannot be negative")
                    except ValueError as e:
                        errors.append({
                            'row': row_num,
                            'error': f"Invalid price '{price}' - {str(e)}"
                        })
                        error_count += 1
                        continue

                    # Download image from URL if provided
                    image_file = None
                    if image_url:
                        try:
                            response = requests.get(
                                image_url, timeout=10, stream=True)
                            if response.status_code == 200:
                                parsed_url = urlparse(image_url)
                                filename = os.path.basename(parsed_url.path)
                                if not filename or '.' not in filename:
                                    filename = f"{title[:30].replace(' ', '_')}.jpg"
                                image_file = ContentFile(
                                    response.content, name=filename)
                            else:
                                errors.append({
                                    'row': row_num,
                                    'error': f'Failed to download image (HTTP {response.status_code})'
                                })
                        except requests.exceptions.RequestException as e:
                            errors.append({
                                'row': row_num,
                                'error': f'Error downloading image - {str(e)}'
                            })

                    # Store validated post data
                    posts_data.append({
                        'title': title,
                        'description': description,
                        'price': price_decimal,
                        'image_file': image_file
                    })

                except Exception as e:
                    errors.append({
                        'row': row_num,
                        'error': f'Unexpected error - {str(e)}'
                    })
                    error_count += 1
                    continue

            # Second pass: Create posts for ALL selected accounts
            for post_data in posts_data:
                for account in accounts:
                    scheduled_time = timezone.now()

                    post = MarketplacePost.objects.create(
                        account=account,
                        title=post_data['title'],
                        description=post_data['description'],
                        price=post_data['price'],
                        scheduled_time=scheduled_time,
                        posted=False
                    )

                    # Assign image if available
                    if post_data.get('image_file'):
                        post.image.save(
                            post_data['image_file'].name,
                            post_data['image_file'],
                            save=True
                        )

                    success_count += 1

            # Prepare response
            num_posts = len(posts_data)
            num_accounts = len(accounts)

            response_data = {
                'success': True,
                'message': f'Successfully created {success_count} posts! ({num_posts} post(s) × {num_accounts} account(s))',
                'stats': {
                    'success_count': success_count,
                    'error_count': error_count,
                    'num_posts': num_posts,
                    'num_accounts': num_accounts
                }
            }

            if errors:
                # Limit to first 10 errors
                response_data['errors'] = errors[:10]
                if len(errors) > 10:
                    response_data['additional_errors'] = len(errors) - 10

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': f'Error processing CSV file: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
