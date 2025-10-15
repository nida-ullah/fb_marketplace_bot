from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MarketplacePostForm, BulkPostUploadForm
from .models import MarketplacePost
import csv
from django.utils import timezone
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse
import os

# Create your views here.


def create_post(request):
    if request.method == 'POST':
        form = MarketplacePostForm(request.POST, request.FILES)
        if form.is_valid():
            # Get form data
            selected_accounts = form.cleaned_data['accounts']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image = form.cleaned_data.get('image')
            image_url = form.cleaned_data.get('image_url')

            # Handle image from file upload or URL
            image_content = None
            image_name = None

            # Priority 1: Uploaded file
            if image:
                image.seek(0)  # Reset file pointer
                image_content = ContentFile(image.read())
                image_name = image.name
            # Priority 2: Image URL
            elif image_url:
                try:
                    response = requests.get(image_url, timeout=10, stream=True)
                    if response.status_code == 200:
                        # Get filename from URL or generate one
                        parsed_url = urlparse(image_url)
                        filename = os.path.basename(parsed_url.path)
                        if not filename or '.' not in filename:
                            # Generate filename from title
                            filename = f"{title[:30].replace(' ', '_')}.jpg"

                        image_content = ContentFile(response.content)
                        image_name = filename
                    else:
                        messages.warning(
                            request,
                            f'⚠️ Failed to download image from URL (HTTP {response.status_code}). Posts created without images.'
                        )
                except requests.exceptions.RequestException as e:
                    messages.warning(
                        request,
                        f'⚠️ Error downloading image: {str(e)}. Posts created without images.'
                    )

            # Create post for each selected account
            posts_created = 0
            for account in selected_accounts:
                post = MarketplacePost.objects.create(
                    account=account,
                    title=title,
                    description=description,
                    price=price,
                    scheduled_time=timezone.now(),  # Auto-set to now
                    posted=False
                )

                # Assign image if available (create separate copy for each post)
                if image_content and image_name:
                    # Reset content file pointer for each save
                    image_content.seek(0)
                    post.image.save(image_name, image_content, save=True)

                posts_created += 1

            messages.success(
                request,
                f'✅ Successfully created {posts_created} post(s) for {len(selected_accounts)} account(s)!'
            )
            return redirect('post_list')
    else:
        form = MarketplacePostForm()

    return render(request, 'postings/create_post.html', {'form': form})


def post_list(request):
    posts = MarketplacePost.objects.all().order_by('-scheduled_time')
    return render(request, 'postings/post_list.html', {'posts': posts})


def bulk_upload_posts(request):
    """View for bulk uploading posts via CSV"""
    if request.method == 'POST':
        form = BulkPostUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            # Validate file extension
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file.')
                return redirect('bulk_upload_posts')

            # Get selected accounts from form
            selected_accounts = list(form.cleaned_data['accounts'])

            # Parse CSV
            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                csv_reader = csv.DictReader(decoded_file)

                success_count = 0
                error_count = 0
                errors = []
                posts_data = []  # Store validated post data

                # First pass: Validate and collect all post data
                for row_num, row in enumerate(csv_reader, start=2):
                    try:
                        # Extract data from CSV (title, description, price, optional image_url)
                        title = row.get('title', '').strip()
                        description = row.get('description', '').strip()
                        price = row.get('price', '').strip()
                        image_url = row.get('image_url', '').strip()

                        # Validate required fields
                        if not all([title, description, price]):
                            errors.append(
                                f"Row {row_num}: Missing required fields (title, description, or price)")
                            error_count += 1
                            continue

                        # Validate price
                        try:
                            price_decimal = float(price)
                            if price_decimal < 0:
                                raise ValueError("Price cannot be negative")
                        except ValueError as e:
                            errors.append(
                                f"Row {row_num}: Invalid price '{price}' - {str(e)}")
                            error_count += 1
                            continue

                        # Download image from URL if provided
                        image_file = None
                        if image_url:
                            try:
                                response = requests.get(
                                    image_url, timeout=10, stream=True)
                                if response.status_code == 200:
                                    # Get filename from URL or generate one
                                    parsed_url = urlparse(image_url)
                                    filename = os.path.basename(
                                        parsed_url.path)
                                    if not filename or '.' not in filename:
                                        # Generate filename from title
                                        filename = f"{title[:30].replace(' ', '_')}.jpg"

                                    # Create ContentFile from response
                                    image_file = ContentFile(
                                        response.content, name=filename)
                                else:
                                    errors.append(
                                        f"Row {row_num}: Failed to download image from URL (HTTP {response.status_code})")
                            except requests.exceptions.RequestException as e:
                                errors.append(
                                    f"Row {row_num}: Error downloading image - {str(e)}")
                            except Exception as e:
                                errors.append(
                                    f"Row {row_num}: Error processing image - {str(e)}")

                        # Store validated post data
                        posts_data.append({
                            'title': title,
                            'description': description,
                            'price': price_decimal,
                            'image_file': image_file
                        })

                    except Exception as e:
                        errors.append(
                            f"Row {row_num}: Unexpected error - {str(e)}")
                        error_count += 1
                        continue

                # Second pass: Create posts for ALL selected accounts
                # Each post will be created for every account
                for post_data in posts_data:
                    for account in selected_accounts:
                        # Set scheduled time to now (immediate posting)
                        scheduled_time = timezone.now()

                        # Create post for this account
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

                # Show results
                if success_count > 0:
                    num_posts = len(posts_data)
                    num_accounts = len(selected_accounts)
                    messages.success(
                        request, f'✅ Successfully created {success_count} posts! ({num_posts} post(s) × {num_accounts} account(s))')

                if error_count > 0:
                    error_message = f'❌ {error_count} error(s) occurred:<br>'
                    # Show first 10 errors
                    error_message += '<br>'.join(errors[:10])
                    if len(errors) > 10:
                        error_message += f'<br>... and {len(errors) - 10} more errors'
                    messages.error(request, error_message)

                if success_count > 0:
                    return redirect('post_list')

            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
                return redirect('bulk_upload_posts')
    else:
        form = BulkPostUploadForm()

    return render(request, 'postings/bulk_upload_posts.html', {'form': form})
