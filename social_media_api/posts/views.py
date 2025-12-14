from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import (
    PostSerializer, 
    PostCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer
)

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit/delete their posts/comments
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing posts
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a specific post"""
        post = self.get_object()
        comments = post.comments.all()
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        """Add a comment to a post"""
        post = self.get_object()
        serializer = CommentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    """
    View to get feed of posts from followed users
    Returns posts from users that the current user follows
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # Or use default pagination
    
    def get_queryset(self):
        # Get users that the current user follows
        following_users = self.request.user.following.all()
        
        # Get posts from followed users, ordered by creation date (newest first)
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        # Optional: Include user's own posts in feed
        # queryset = queryset | Post.objects.filter(author=self.request.user)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Check if user is following anyone
        if not request.user.following.exists():
            return Response({
                "message": "You are not following anyone yet. Follow some users to see their posts here!",
                "suggestions": User.objects.exclude(id=request.user.id).order_by('?')[:5].values('id', 'username', 'first_name', 'last_name')
            }, status=status.HTTP_200_OK)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
