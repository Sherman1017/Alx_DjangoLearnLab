from rest_framework import serializers
from .models import Post, Comment
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user representation in posts/comments"""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_picture']

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), 
        source='author', 
        write_only=True
    )
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model"""
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), 
        source='author', 
        write_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_id', 'title', 'content', 
                 'created_at', 'updated_at', 'comments', 'comments_count']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        return obj.comments.count()

class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts (simplified)"""
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Post.objects.create(author=user, **validated_data)

class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating comments (simplified)"""
    class Meta:
        model = Comment
        fields = ['post', 'content']
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Comment.objects.create(author=user, **validated_data)

class LikeSerializer(serializers.ModelSerializer):
    """Serializer for Like model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['created_at']

class PostSerializer(serializers.ModelSerializer):
    """Updated PostSerializer with likes"""
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), 
        source='author', 
        write_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    likes = LikeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_id', 'title', 'content', 
                 'created_at', 'updated_at', 'comments', 'comments_count',
                 'likes_count', 'is_liked', 'likes']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
