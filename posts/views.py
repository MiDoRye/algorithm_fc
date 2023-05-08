from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=204)


class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        comments = Comment.objects.filter(post=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, author=request.user)
        return Response(serializer.data)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, post=post_id)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, post=post_id)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=204)
