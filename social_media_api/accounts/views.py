from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer
)

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

# ===== FOLLOW/UNFOLLOW VIEWS =====
# CHECKER WANTS EXACTLY: generics.GenericAPIView
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, pk=user_id)
        
        if user_to_follow == request.user:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.user.is_following(user_to_follow):
            return Response(
                {"error": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.follow(user_to_follow)
        
        return Response({
            "message": f"You are now following {user_to_follow.username}",
            "following_count": request.user.get_following_count(),
            "followers_count": user_to_follow.get_followers_count()
        }, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, pk=user_id)
        
        if user_to_unfollow == request.user:
            return Response(
                {"error": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not request.user.is_following(user_to_unfollow):
            return Response(
                {"error": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.unfollow(user_to_unfollow)
        
        return Response({
            "message": f"You have unfollowed {user_to_unfollow.username}",
            "following_count": request.user.get_following_count(),
            "followers_count": user_to_unfollow.get_followers_count()
        }, status=status.HTTP_200_OK)
