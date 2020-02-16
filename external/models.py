from django.db import models
from django.urls import reverse

from accounts.models import PiroUser

class Recruitment(models.Model):
    title = models.CharField(max_length=50, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    img = models.ImageField(blank=True, upload_to="recruit", verbose_name='이미지')
    created_at = models.DateField(auto_now_add=True)

    author = models.ForeignKey(PiroUser, on_delete=models.CASCADE, verbose_name='글쓴이')

    def get_absolute_url(self):
        return reverse('home:recruit_detail', args=[self.pk])


class Portfolio(models.Model):
    title = models.CharField(max_length=50, verbose_name='프로젝트 이름')
    team = models.CharField(max_length=50, verbose_name='팀이름')
    content = models.TextField(verbose_name='내용')
    image = models.ImageField(blank=True, upload_to="portfolio", verbose_name="사진")
    pironumber = models.PositiveIntegerField(verbose_name="기수")