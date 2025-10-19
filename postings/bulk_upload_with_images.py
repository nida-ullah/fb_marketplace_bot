"""
Bulk Upload with Images - Enhanced API View
This allows users to upload TXT + multiple image files
Images are automatically matched BY ORDER (1st image → 1st product, 2nd image → 2nd product, etc.)
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MarketplacePost
from accounts.models import FacebookAccount
from django.utils import timezone


class BulkUploadWithImagesView(APIView):
    """
    Accept TXT + multiple image files (no ZIP needed!)
    Images are automatically matched by ORDER:
    - 1st image → 1st product
    - 2nd image → 2nd product
    - 3rd image → 3rd product

    TXT Format (each product has 3 lines + blank line):
    Title
    Description
    Price

    Title 2
    Description 2
    Price 2
    """

    def post(self, request):
        # Get files
        txt_file = request.FILES.get('txt_file')
        image_files = request.FILES.getlist('images')  # Multiple image files
        account_ids = request.data.getlist('account_ids[]')

        # Validation
        if not txt_file:
            return Response(
                {'error': 'TXT file is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not account_ids:
            return Response(
                {'error': 'At least one account must be selected'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get accounts
        try:
            accounts = FacebookAccount.objects.filter(
                id__in=account_ids
            )
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

        # Parse TXT file
        try:
            decoded_file = txt_file.read().decode('utf-8')
            lines = decoded_file.strip().split('\n')

            success_count = 0
            error_count = 0
            errors = []
            posts_data = []

            # Parse TXT file - each product has 3 lines (title, description, price) + blank line
            product_index = 0
            i = 0
            while i < len(lines):
                line_num = i + 1  # For display purposes

                # Skip empty lines at the start
                if not lines[i].strip():
                    i += 1
                    continue

                try:
                    # Get 3 lines for one product
                    if i + 2 >= len(lines):
                        errors.append({
                            'line': line_num,
                            'error': 'Incomplete product data (need 3 lines: title, description, price)'
                        })
                        error_count += 1
                        break

                    title = lines[i].strip()
                    description = lines[i + 1].strip()
                    price_str = lines[i + 2].strip()

                    # Validate required fields
                    if not all([title, description, price_str]):
                        errors.append({
                            'line': line_num,
                            'error': 'Missing required fields'
                        })
                        error_count += 1
                        i += 4  # Skip to next product (3 lines + blank line)
                        product_index += 1
                        continue

                    # Validate price
                    try:
                        price_decimal = float(price_str)
                        if price_decimal < 0:
                            raise ValueError("Price cannot be negative")
                    except ValueError:
                        errors.append({
                            'line': line_num + 2,
                            'error': f"Invalid price: {price_str}"
                        })
                        error_count += 1
                        i += 4
                        product_index += 1
                        continue

                    # Get image by ORDER (index matches product index)
                    image_file = None
                    if image_files and product_index < len(image_files):
                        image_file = image_files[product_index]

                    posts_data.append({
                        'title': title,
                        'description': description,
                        'price': price_decimal,
                        'image_file': image_file
                    })

                    product_index += 1
                    i += 4  # Move to next product (3 lines + blank line)

                except Exception as e:
                    errors.append({
                        'line': line_num,
                        'error': str(e)
                    })
                    error_count += 1
                    i += 4
                    product_index += 1

            # Create posts for all accounts
            for post_data in posts_data:
                for account in accounts:
                    post = MarketplacePost.objects.create(
                        account=account,
                        title=post_data['title'],
                        description=post_data['description'],
                        price=post_data['price'],
                        scheduled_time=timezone.now(),
                        posted=False
                    )

                    if post_data.get('image_file'):
                        post.image.save(
                            post_data['image_file'].name,
                            post_data['image_file'],
                            save=True
                        )

                    success_count += 1

            response_data = {
                'success': True,
                'message': f'Created {success_count} posts!',
                'stats': {
                    'success_count': success_count,
                    'error_count': error_count,
                    'num_posts': len(posts_data),
                    'num_accounts': len(accounts)
                }
            }

            if errors:
                response_data['errors'] = errors[:10]
                if len(errors) > 10:
                    response_data['additional_errors'] = len(errors) - 10

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Error processing TXT file: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
