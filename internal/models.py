import os

from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

from accounts.models import PiroUser

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='제목')
    body = RichTextUploadingField(verbose_name='내용')
    tag = models.CharField(max_length=30)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(PiroUser, on_delete=models.CASCADE, verbose_name='글쓴이')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = RichTextUploadingField(verbose_name='내용')

    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(PiroUser, on_delete=models.CASCADE)

    like_user_set = models.ManyToManyField(PiroUser, blank=True, related_name='like_user_set',
                                           through='Like')

    like_num = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.post}의 댓글'

    @property
    def like_count(self):
        return self.like_user_set.count()

    def delete(self):
        os.remove(self.file.path)
        return super(Comment, self).delete()

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, default=None)
    content = models.TextField(verbose_name='내용')

    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(PiroUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.comment}의 답글'


class Like(models.Model):
    user = models.ForeignKey(PiroUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class InfoBook(models.Model):
    user = models.ForeignKey(PiroUser, on_delete=models.CASCADE)
    current_work = models.CharField(max_length=100)
    piro_no = models.PositiveIntegerField()
    history = models.TextField()


class Notification(models.Model):
    TYPE_CHOICES = (
        ('좋아요', '좋아요'),
        ('댓글', '댓글'),
        ('답글', '답글'),
    )
    creator = models.ForeignKey(PiroUser, on_delete=models.CASCADE, related_name='creator')
    to = models.ForeignKey(PiroUser, on_delete=models.CASCADE, related_name='to')
    myid = models.CharField(max_length=250, null=True, blank= True)

    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    checked = models.BooleanField(default=False)


