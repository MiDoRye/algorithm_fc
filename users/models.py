from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, user_name, email, password=None):
        if not user_name:
            raise ValueError("아이디를 입력해주세요!")
        if not email:
            raise ValueError('이메일 주소를 입력해주세요!')
        
        user = self.model(
            user_name = user_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, user_name, email, password=None):
        user = self.create_user(
            user_name=user_name,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        
        return user

# 기본 사용자 모델
class User(AbstractBaseUser):
    user_name = models.CharField('ID', max_length=30, unique=True, error_messages={"unique": "이미 사용 중이거나 탈퇴한 사용자의 아이디입니다!"})
    email = models.EmailField('EMAIL', max_length=255, unique=True, error_messages={"unique": "이미 사용 중이거나 탈퇴한 사용자의 이메일입니다!"})
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField("계정 생성일", auto_now_add=True)
    last_password_changed = models.DateTimeField("비밀번호 마지막 변경일", auto_now=True)
    withdraw = models.BooleanField("회원 비활성화", default=False)
    withdraw_at = models.DateTimeField("계정 탈퇴일", null=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ["email",]

    def __str__(self):
        return f"[ID]{self.user_name}"

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin


# 사용자 프로필 모델
class UserProfile(models.Model):
    profile_image = models.ImageField("PROFILE IMAGE", default="default_profile_pic.jpg", upload_to="profile_pics", blank=True)
    nickname = models.CharField("NICKNAME", max_length=10, null=True, unique=True, error_messages={"unique": "이미 사용 중이거나 탈퇴한 사용자의 닉네임입니다!"})
    age = models.IntegerField("AGE", null=True)
    # MALE = "male"
    # FEMALE = "female"
    # OTHER = "other"
    gender_choices = [("MALE", "male"), ("FEMALE", "female"), ("OTHER", "other"),]
    gender = models.CharField("GENDER", max_length=6, null=True, choices=gender_choices,)
    introduction = models.TextField(null=True, default="안녕하세요!")
    review_cnt = models.PositiveIntegerField("Review cnt", default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="USER", related_name="user_profile")

    followings = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers")
    
    def __str__(self):
        return f"[ID]{self.user.user_name}, [NICKNAME]{self.nickname}"

    @property
    def review_count_add(self):
        self.review_cnt += 1
        self.save()

    @property
    def review_count_remove(self):
        self.review_cnt -= 1
        self.save()