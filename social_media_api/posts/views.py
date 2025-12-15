from rest_framework import viewsets, permissions, filters, status, generics
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
from accounts.models import CustomUser

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
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
        post = self.get_object()
        serializer = CommentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# ===== FEED VIEW =====
# CHECKER: View that generates feed based on posts from users the current user follows
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get users that the current user follows
        following_users = self.request.user.following.all()
        
        # Get posts from followed users, ordered by creation date (most recent first)
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

# ===== LIKE FUNCTIONALITY =====
from .models import Like
from notifications.models import Notification

class LikePostView(generics.GenericAPIView):
    """
    View to like a post
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        
        # Check if already liked
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response(
                {"error": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create like
        like = Like.objects.create(user=request.user, post=post)
        
        # Create notification for post author (if not liking own post)
        if post.author != request.user:
            Notification.create_notification(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )
        
        return Response({
            "message": "Post liked successfully",
            "likes_count": post.likes.count(),
            "like_id": like.id
        }, status=status.HTTP_201_CREATED)

class UnlikePostView(generics.GenericAPIView):
    """
    View to unlike a post
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        
        # Check if liked
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response(
                {"error": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete like
        like.delete()
        
        return Response({
            "message": "Post unliked successfully",
            "likes_count": post.likes.count()
        }, status=status.HTTP_200_OK)

# Add like/unlike actions to PostViewSet
PostViewSet.like = LikePostView.as_view()
PostViewSet.unlike = UnlikePostView.as_view()
