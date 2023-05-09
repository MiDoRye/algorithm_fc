from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView, LikeView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post_list_create'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment_list_create'),
    path('<int:post_id>/comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment_detail'),
    #'''--------------------------추가된 부분: 좋아요 기능-------------------이주한-'''
    path('<int:post_id>/like/', LikeView.as_view(), name='like_view'),
    #'''--------------------------------------------------------------------------'''
]