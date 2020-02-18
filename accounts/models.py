from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class PiroUserManager(BaseUserManager):
    def create_user(self, email, name, username, phone_no, piro_no, img_profile, left_over, github, password=None):
        if not email:
            raise ValueError('이메일을 입력하시오.')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            username = username,
            phone_no = phone_no,
            piro_no = piro_no,
            img_profile = img_profile,
            left_over = left_over,
            github = github,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        name = '운영진'
        phone_no = '010-0000-0000'
        piro_no = 99999999
        img_profile = None
        left_over = 99999999
        github = 'https://github.com/pirogramming/'
        user = self.create_user(
            email,
            password=password,
            name=name,
            username=username,
            phone_no=phone_no,
            piro_no=piro_no,
            img_profile=img_profile,
            left_over=left_over,
            github = github,
        )
        user.is_active=True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class PiroUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name='이메일')
    name = models.CharField(max_length=10, verbose_name='이름 (본명)')
    username = models.CharField(max_length=10, unique=True, verbose_name='아이디/ 닉네임')
    phone_no = models.CharField(max_length=20, verbose_name='전화번호')
    piro_no = models.PositiveIntegerField(verbose_name='기수')
    img_profile = models.ImageField(upload_to="user", blank= True, default=None, verbose_name='프로필 사진')
    left_over = models.PositiveIntegerField(blank=True, default=200000, verbose_name='보증금')
    github = models.URLField(verbose_name='깃허브 주소', blank=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = PiroUserManager()

    def __str__(self):
        return f'{self.name}'

class Bookmark(models.Model):
    pirouser = models.ForeignKey(PiroUser, on_delete=models.CASCADE)
    bookmark_title = models.CharField(max_length=250)
    bookmark_num = models.CharField(max_length=250)
    bookmark_type = models.CharField(max_length=250)
    
    def __str__(self):
        return f'{self.pirouser}의 스크랩- {self.bookmark_num}'