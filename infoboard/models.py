import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from accounts.models import PiroUser


class Info(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(PiroUser, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.title


class Files(models.Model):
    def date_upload_to(self, filename):
        # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
        ymd_path = timezone.now().strftime('%Y/%m%d')
        # 길이 32 인 uuid 값
        uuid_name = uuid4().hex
        # 확장자 추출
        #extension = os.path.splitext(filename)[-1].lower()
        # 결합 후 return
        return '/'.join([
            'info',
            'file',
            ymd_path,
            uuid_name + filename# + extension,
        ])

    info = models.ForeignKey(Info, on_delete=models.CASCADE)
    file = models.FileField(upload_to=date_upload_to)
    filename = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.info}의 파일'

    def delete(self):
        os.remove(self.file.path)
        return super(Files, self).delete()