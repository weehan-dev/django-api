from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from meeting.models import Team
# Create your models here.


class YHDUserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None):
        if not username and not email:
            raise ValueError('ID, Email은 필수입니다.')

        user = self.model(
            username=username,
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email):
        if not username and not email:
            raise ValueError('ID, Email은 필수입니다.')
        user = self.create_user(username, password, email)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    objects = YHDUserManager()

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)

    username = models.CharField(max_length=30, null=False, unique=True, verbose_name='아이디')
    email = models.EmailField(null=False, verbose_name='이메일', blank=False)

    is_certificated = models.BooleanField(default=False, verbose_name='대학 인증') # 대학 인증 ?
    is_matched = models.BooleanField(default=False, verbose_name='매칭 중')  # 매칭 중 ?
    is_warned = models.BooleanField(default=False, verbose_name='경고')   # 경고 회원 ?
    is_suspended = models.BooleanField(default=False, verbose_name='정지 회원')    # 정지 회원 ?
    is_delete = models.BooleanField(default=False, verbose_name='삭제된 회원')   # 삭제 회원 ?
    is_active = models.BooleanField(default=True, verbose_name='활동 회원')   # 활동 회원 ?

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser

    class Meta:
        db_table = 'users'
        verbose_name = '유저'
        verbose_name_plural = '유저들'


GENDER = (
    ('M', '남자'),
    ('F', '여자')
)

UNIV_LIST = (
    ('Hanyang', '한양대학교'),
    ('Sejong', '세종대학교')
)

RELIGION = (
    ('Christian', '기독교'),
    ('Catholic', '천주교'),
    ('Buddhism', '불교'),
    ('None', '무교'),
    ('Other', '그 외')
)


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True) # 연결

    name = models.CharField(max_length=20, null=False)
    gender = models.CharField(max_length=1, choices=GENDER, null=False)
    univ = models.CharField(max_length=15, choices=UNIV_LIST, null=False)
    latitude = models.DecimalField(decimal_places=7, max_digits=9)
    longitude = models.DecimalField(decimal_places=7, max_digits=10)
    avatar = models.ImageField(null=True)

    height = models.PositiveSmallIntegerField(null=True)
    weight = models.PositiveSmallIntegerField(null=True)
    religion = models.CharField(max_length=10, null=False)
    is_smoker = models.BooleanField(null=False)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


