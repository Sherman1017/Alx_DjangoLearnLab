from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import UserProfileSerializer, UserRegistrationSerializer
from .models import CustomUser

User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing user profiles and follow actions
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        """Follow a user"""
        user_to_follow = get_object_or_404(User, pk=pk)
        
        # Can't follow yourself
        if user_to_follow == request.user:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already following
        if request.user.is_following(user_to_follow):
            return Response(
                {"error": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Follow the user
        request.user.follow(user_to_follow)
        
        return Response({
            "message": f"You are now following {user_to_follow.username}",
            "following_count": request.user.get_following_count(),
            "followers_count": user_to_follow.get_followers_count()
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request, pk=None):
        """Unfollow a user"""
        user_to_unfollow = get_object_or_404(User, pk=pk)
        
        # Can't unfollow yourself
        if user_to_unfollow == request.user:
            return Response(
                {"error": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if actually following
        if not request.user.is_following(user_to_unfollow):
            return Response(
                {"error": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Unfollow the user
        request.user.unfollow(user_to_unfollow)
        
        return Response({
            "message": f"You have unfollowed {user_to_unfollow.username}",
            "following_count": request.user.get_following_count(),
            "followers_count": user_to_unfollow.get_followers_count()
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        """Get list of followers for a user"""
        user = self.get_object()
        followers = user.followers.all()
        page = self.paginate_queryset(followers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        """Get list of users followed by a user"""
        user = self.get_object()
        following = user.following.all()
        page = self.paginate_queryset(following)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)
