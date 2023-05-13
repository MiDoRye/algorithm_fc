from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from users.serializers import UserSerializer, UserDetailSerializer
from users.models import User
# ===================================== email 요청 import 추가 =============================
import traceback
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
import jwt
from django.conf import settings
secret_key = settings.SECRET_KEY


class SignUpView(APIView):
    """
    사용자 가입 기능을 정의한 APIView 클래스입니다. POST 요청을 처리하며, 유효한 시리얼라이저인 경우 새로운 사용자를 생성합니다.
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    사용자에 대한 CRUD 기능을 구현하는 APIView 입니다.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if str(request.user) == user.email:
            serializer = UserDetailSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)
        # serializer = UserDetailSerializer(user, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if str(request.user) == user.email:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)
        # user.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)


class UserActivate(APIView):
    """
    사용자 계정 활성화를 위한 APIView를 구현한 코드입니다.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        try:
            # JWT 토큰 검증
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            if payload['user_id'] != user.id:
                return Response('토큰이 올바르지 않습니다', status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response('만료된 토큰입니다', status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response('잘못된 토큰입니다', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(traceback.format_exc())

        if user is not None:
            user.is_active = True
            user.save()
            return Response(user.email + '계정이 활성화 되었습니다', status=status.HTTP_200_OK)
        else:
            return Response('사용자를 찾을 수 없습니다', status=status.HTTP_400_BAD_REQUEST)


class FollowView(APIView):
    """
    사용자간의 팔로우/언팔로우 기능을 구현하는 FollowView 클래스를 정의합니다.
    """

    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me == you.email:
            if me in you.followers.all():
                you.followers.remove(me)
                return Response("unfollow했습니다.", status=status.HTTP_200_OK)
            else:
                you.followers.add(me)
                return Response("follow했습니다.", status=status.HTTP_200_OK)
        else:
            return Response('본인을 팔로우 하는 사람이 어딨어?!', status=status.HTTP_400_BAD_REQUEST)
