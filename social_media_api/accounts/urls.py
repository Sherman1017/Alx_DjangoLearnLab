from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView
)
from .user_views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
    
    # Follow endpoints (alternative to ViewSet actions)
    path('follow/<int:user_id>/', UserProfileView.as_view({'post': 'follow'}), name='follow'),
    path('unfollow/<int:user_id>/', UserProfileView.as_view({'post': 'unfollow'}), name='unfollow'),
]
