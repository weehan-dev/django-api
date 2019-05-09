from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=30, null=False)
    password = models.TextField()
    email = models.CharField(max_length=100, null=False)

    isCertificated = models.BooleanField(default=False) # 대학 인증 ?
    isMatched = models.BooleanField(default=False)  # 매칭 중 ?
    isWarned = models.BooleanField(default=False)   # 경고 회원 ?
    isSuspended = models.BooleanField(default=False)    # 정지 회원 ?
    isDelete = models.BooleanField(default=False)   # 삭제 회원 ?

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


GENDER = (
    ('M', '남'),
    ('F', '여')
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

    user = models.OneToOneField(User, on_delete=models.CASCADE) # 연결

    name = models.CharField(max_length=20, null=False)
    gender = models.CharField(max_length=1, choices=GENDER, null=False)
    univ = models.CharField(max_length=15, choices=UNIV_LIST, null=False)
    location = models.ForeignKey()
    avatar = models.ImageField(upload_to="/static/profile/%Y/%M")

    height = models.PositiveSmallIntegerField(null=True)
    weight = models.PositiveSmallIntegerField(null=True)
    religion = models.CharField(max_length=10, null=False)
    isSmoker = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





