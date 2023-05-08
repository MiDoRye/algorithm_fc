from django.db import models


class Post(models.Model):
    '''
    id : 데이터 고유 id 입니다(pk).
    title : 포스팅 제목입니다.
    image : 포스팅 이미지입니다.
    contents : 포스팅 내용입니다.
    created_at : 포스팅 생성 시간입니다.
    updated_at : 포스팅의 마지막 수정 시간입니다.
    user_id : 사용자 테이블과 FK로 관계형성이 되어야합니다.
    '''
