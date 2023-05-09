from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post_list_create'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/comments/',
        CommentListCreateView.as_view(), name='comment_list_create'),
    path('<int:post_id>/comments/<int:comment_id>/',
        CommentDetailView.as_view(), name='comment_detail'),
]