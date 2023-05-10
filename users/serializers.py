from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from posts.serializers import PostSerializer


class UserSerializer(serializers.ModelSerializer):
    user_posts = PostSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
        
    def update(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #'''----------------추가된 부분: 이미지 추가 기능---------------이주한-'''
        fields = ("id", "email", "name", "age", "gender", "introduction", "image")
        #'''----------------fields에 "image"를 추가했습니다.------------------'''

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        token['gender'] = user.gender
        token['age'] = user.age
        return token