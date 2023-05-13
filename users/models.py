from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    """
    BaseUserManager 클래스를 상속받아 UserManager 클래스를 정의합니다.
    """

    def create_user(self, email, password=None):
        # email 값이 없으면 에러를 발생시킵니다.
        if not email:
            raise ValueError('Users must have an email address')

        # email 값을 소문자로 정규화한 후, 모델 객체를 생성합니다.
        user = self.model(
            email=self.normalize_email(email),
        )
        # 입력받은 password 값을 암호화하여 저장합니다.
        user.set_password(password)
        user.save(using=self._db)
        return user
    # 슈퍼 유저 생성 메소드를 정의합니다.

    def create_superuser(self, email, password=None):
        # 일반 유저 생성 메소드를 호출하여 유저 객체를 생성합니다.
        user = self.create_user(
            email,
            password=password,
        )
        # 유저 객체에 관리자 권한을 부여합니다.
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    name = models.CharField(max_length=100, default="test_user")
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    gender_choices = [
        (MALE, "male"),
        (FEMALE, "female"),
        (OTHER, "other"),
    ]
    gender = models.CharField(
        max_length=6,
        choices=gender_choices,
        default=OTHER,
    )
    age = models.IntegerField(null=True, default=20)
    introduction = models.TextField(null=True, default="소개글 입니다.")
    followings = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers', blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(blank=True, upload_to='%Y/%m/%d/')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # Simplest possible answer: All admins are staff
        return self.is_admin
