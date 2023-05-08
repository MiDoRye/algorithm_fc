from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, UserProfileSerializer


class PostView(APIView):
    def get(self, request, pk=None):
        '''pk 값의 유무에 따라 게시글 목록 혹은 게시글의 상세 정보를 response 합니다.'''
        # pk가 있을 경우
        '''
        {
            title: "post 제목",
            content: "post 내용"
        }
        '''
        # pk가 없을 경우
        '''
        [
            {
                title: "post 제목",
                content: "post 내용"
            },
            {
                title: "post 제목",
                content: "post 내용"
            },
            {
                title: "post 제목",
                content: "post 내용"
            },
                        .
                        .
                        .
                        .
                        .
        ]
        '''
        return Response({'message': 'get 요청입니다.'})
    
    def post(self, request):
        '''내용을 입력받아 게시글을 생성합니다.'''
        
        return Response({'message': 'post 요청입니다.'})
    
    def put(self, request):
        '''게시글을 수정합니다.'''
        
        return Response({'message': 'put 요청입니다.'})

    def delete(self, request):
        '''게시글을 삭제합니다.'''
        
        return Response({'message': 'delete 요청입니다.'})