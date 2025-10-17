from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import MarketplacePost
from .serializers import MarketplacePostSerializer


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


class MarketplacePostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a marketplace post"""
    queryset = MarketplacePost.objects.all()
    serializer_class = MarketplacePostSerializer
    permission_classes = [IsAuthenticated]
