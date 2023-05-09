from rest_framework import serializers
from .models import Post, Comment, PageModel


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):   # 페이지네이션
    class Meta:
        model = PageModel
        fields = '__all__'
