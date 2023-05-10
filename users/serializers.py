from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from posts.serializers import PostSerializer


from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.urls import reverse
from rest_framework_jwt.settings import api_settings


class UserSerializer(serializers.ModelSerializer):
    user_posts = PostSerializer(many=True, read_only=True)
    class Meta:
        model = User
        #-----------------------------수정 - 사용자 정보 조회시 조회될 필드들 수정------------------------이주한---
        fields = ("id", "email", "name", "age", "gender", "introduction", "image", "user_posts", "followings")


    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        # is_active = False로 지정해주어 email 인증을 하기 전에 접속 불가능하게 설정
        user.is_active = False
        user.save()

        # jwt 토큰 생성
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # email을 생성하여 보내는 부분
        message = f"{user.email}님 링크를 클릭해 계정을 활성화 해주세요\n"
        message += f"http://127.0.0.1:8000{reverse('user:activate', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': token})}"
        email = EmailMessage('test', message, to=[user.email])
        email.send()

        return validated_data
    
        
    def update(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #'''----------------사용자 상세 페이지 이미지 추가 기능---------------이주한-'''
        fields = ("id", "email", "name", "age", "gender", "introduction", "image")
        #'''----------------------------------------------------------------------'''

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        token['gender'] = user.gender
        token['age'] = user.age
        return token