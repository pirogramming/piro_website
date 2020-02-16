from django import forms
from .models import Post, Comment, Reply


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'tag']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class ReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = '댓글을 입력하세요.'

    class Meta:
        model = Reply
        fields = ['content']