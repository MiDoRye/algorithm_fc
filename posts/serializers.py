from rest_framework import serializers
from .models import Post, Comment, PageModel


class CommentSerializer(serializers.ModelSerializer):
    """
     Comment 모델을 직렬화할 때 사용하는 CommentSerializer 클래스를 정의한 것입니다.
    """
    # author = serializers.ReadOnlyField(source='author.username')
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.email

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """
     게시글(Post) 모델을 위한 Serializer 클래스인 PostSerializer를 정의하고 있습니다.
    """
    # author = serializers.ReadOnlyField(source='author.username')
    author = serializers.SerializerMethodField()
    # comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    # 게시글 작성자의 이메일 주소를 출력
    def get_author(self, obj):
        return obj.author.email

    # 게시글에 달린 좋아요 수를 출력
    def get_likes_count(self, obj):
        return obj.likes.count()

    # 게시글에 달린 댓글 수를 출력
    def get_comments_count(self, obj):
        return obj.comments.count()

    # 사용할 필드
    class Meta:
        model = Post
        fields = ("pk", "title", "content", "updated_at",
                  "author", "likes_count", "comments_count")


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Post 모델의 detail 정보를 JSON 형태로 변환하기 위한 Serializer입니다.
    """
    # author = serializers.ReadOnlyField(source='author.username')
    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True, required=False)
    # 'required=False'는 게시글 put 메소드 실행시 likes 필드를 필수로 채우지 않아도 진행을 할 수 있도록 해줍니다.

    # 게시글 작성자의 이메일 주소를 출력
    def get_author(self, obj):
        return obj.author.email

    # 게시글에 달린 좋아요 수를 출력
    def get_likes_count(self, obj):
        return obj.likes.count()

    # 게시글에 달린 댓글 수를 출력
    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = '__all__'


# 페이지네이션
class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageModel
        fields = '__all__'
