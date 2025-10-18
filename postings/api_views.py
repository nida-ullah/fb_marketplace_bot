from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import MarketplacePost
from .serializers import MarketplacePostSerializer
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse
import os


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
