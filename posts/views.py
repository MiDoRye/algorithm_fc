from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post, Comment, PageModel
from .serializers import PostSerializer, CommentSerializer, PageSerializer, PostDetailSerializer


class PostListCreateView(APIView):
    """
    게시글(Post) 목록 조회와 게시글 생성을 담당하는 APIView 입니다.
    """
    permission_classes = [IsAuthenticated]  # 인증된 사용자만

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
    """
    Post에 대한 조회 조회(GET), 수정(PUT), 삭제(DELETE)를 담당하는 뷰 입니다.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if request.user == post.author:
            serializer = PostDetailSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)
        # serializer = PostSerializer(post, data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        # self.check_object_permissions(request, post)
        if request.user == post.author:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)


class CommentListCreateView(APIView):
    """
    댓글의 목록을 보여주고, 새로운 댓글을 작성하는 데 사용되는 APIView 입니다.
    """
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
    """
    Comment 모델의 특정 댓글에 대한 수정과 삭제를 처리하는 뷰입니다.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, post=post_id)
        # self.check_object_permissions(request, comment)
        if request.user == comment.author:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)
        # serializer = CommentSerializer(comment, data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)

    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, post=post_id)
        # self.check_object_permissions(request, comment)
        if request.user == comment.author:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView):
    # 이 API는 인증이 필요하지 않으므로 권한 클래스를 지정하지 않음
    def post(self, request, post_id):
        # 요청된 post_id에 해당하는 게시물을 가져옴
        post = get_object_or_404(Post, pk=post_id)
        print(request.user)
        # 해당 게시물에 현재 사용자가 좋아요를 눌렀는지 확인
        if request.user in post.likes.all():
            # 좋아요를 누른 적이 있으면 좋아요 취소
            post.likes.remove(request.user)
            return Response("좋아요 취소", status=status.HTTP_200_OK)
        else:
            # 좋아요를 누른 적이 없으면 좋아요 추가
            post.likes.add(request.user)
            return Response("좋아요", status=status.HTTP_200_OK)


class Pagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_number'  # Default: 'page'
    page_size_query_param = 'page_size'  # Default: 'page_size'
    max_page_size = 100


class PageView(APIView):
    pagination_class = Pagination

    def get(self, request, format=None):
        queryset = PageModel.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PageSerializer(queryset, many=True)
        return Response(serializer.data)
