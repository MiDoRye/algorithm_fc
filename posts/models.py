from django.db import models
# from django.conf import settings
from users.models import User


class Post(models.Model):
    """
    게시글(Post)모델의 정의
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True, related_name="like_posts")

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    댓글(Comment)모델의 정의
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
        # return "{}의 댓글".format(self.author)


class PageModel(models.Model):
    """
    Pagenation 모델의 정의
    """
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
