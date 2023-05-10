from rest_framework import serializers
from .models import Post, Comment, PageModel


class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.email

    class Meta:
        model = Comment
        fields = '__all__'

# ---------------------수정된 부분: 좋아요 카운트, 댓글 카운트(댓글 내용과 좋아요한 유저의 정보는 불러지지 않게 수정)-----------이주한-


class PostSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')
    author = serializers.SerializerMethodField()
    # comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.email

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = ("pk", "title", "content", "updated_at",
                  "author", "likes_count", "comments_count")
# -------------------------------------------------------------------------------------------------------------------------------


# ----------추가된 부분: 게시글 상세 페이지에 사용될 serializer를 추가했습니다.------------------
# -----기능: 일반 PostSerializer기능에 더해 댓글내용과 좋아요를 누른 사용자들의 이메일이 불러와 집니다.-------이주한-
class PostDetailSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')
    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True, required=False)
    # 'required=False'는 게시글 put 메소드 실행시 likes 필드를 필수로 채우지 않아도 진행을 할 수 있도록 해줍니다.

    def get_author(self, obj):
        return obj.author.email

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = '__all__'

# --------------------------------------------------------------------------------------------------------------


# 페이지네이션
class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageModel
        fields = '__all__'
