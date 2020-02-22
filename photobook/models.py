import os
from uuid import uuid4

from django.db import models

# Create your models here.
from django.utils import timezone

from accounts.models import PiroUser


class Photobook(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(PiroUser, on_delete=models.CASCADE)
    text = models.TextField()

    def date_upload_to(self, filename):
        # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
        ymd_path = timezone.now().strftime('%Y/%m%d')
        # 길이 32 인 uuid 값
        uuid_name = uuid4().hex
        # 확장자 추출
        extension = os.path.splitext(filename)[-1].lower()
        # 결합 후 return
        return '/'.join([
            'photobook',
            'thumbnail',
            ymd_path,
            uuid_name + extension,
        ])

    thumbnail = models.ImageField(upload_to=date_upload_to)

    def delete(self):
        os.remove(self.thumbnail.path)
        return super(Photobook, self).delete()

    def __str__(self):
        return f'사진첩- {self.title}'

class Images(models.Model):
    def date_upload_to(self, filename):
        # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
        ymd_path = timezone.now().strftime('%Y/%m%d')
        # 길이 32 인 uuid 값
        uuid_name = uuid4().hex
        # 확장자 추출
        extension = os.path.splitext(filename)[-1].lower()
        # 결합 후 return
        return '/'.join([
            'photobook',
            'image',
            ymd_path,
            uuid_name + extension,
        ])

    photobook = models.ForeignKey(Photobook, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=date_upload_to)
    
    def __str__(self):
        return f'<{self.photobook}>의 사진'
    
    def delete(self):
        os.remove(self.image.path)
        return super(Images, self).delete()
