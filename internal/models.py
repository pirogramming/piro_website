import os

from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse

from accounts.models import PiroUser

class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='제목')
    body = RichTextField(verbose_name='내용')
    tag = models.CharField(max_length=30)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(PiroUser, on_delete=models.CASCADE, verbose_name='글쓴이')

    #def get_absolute_url(self):
        #return reverse('intranet:post_detail', args=[self.pk])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = RichTextField(verbose_name='내용')

    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(PiroUser, on_delete=models.CASCADE)

    like_user_set = models.ManyToManyField(PiroUser, blank=True, related_name='like_user_set',
                                           through='Like')

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


class Like(models.Model):
    user = models.ForeignKey(PiroUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)