
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from internal.forms import QuestionForm, CommentForm, ReplyForm
from .models import Post, Comment


def mainscreen(request):
    return render(request, 'main_intranet.html')

def qna(request):
    return render(request, 'internal/qboard.html')

def q_new(request, post=None):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("intranet:qna")
        else:
            return redirect("home:home")
    else:
        form = QuestionForm(instance=post)
        return render(request, 'internal/qcreate.html', {
            'form': form,
        })

def q_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = post.comment_set.all().order_by('-like_user_set')
    comment_no = comment.count()
    form = CommentForm()
    form2 = ReplyForm()
    return render(request,'internal/qdetail.html', {
        'post': post,
        'comment': comment,
        'comment_no': comment_no,
        'form': form,
        'form2': form2,
    })


def comment_create(request, pk, comment=None):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('intranet:q_detail', post.pk)
    else:
        form = CommentForm(instance=comment)
        return render(request, 'internal/qdetail.html', {
            'form': form,
        })


def reply_create(request, pk, cmt_pk, reply=None):
    post = Post.objects.get(pk=pk)
    comment = Comment.objects.get(pk=cmt_pk)
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.author = request.user
            reply.save()
            return redirect('intranet:q_detail', post.pk)
    else:
        form2 = ReplyForm(instance=reply)
        return render(request, 'internal/qdetail.html', {
            'form2': form2,
        })


@login_required
@require_POST  # 해당 뷰는 POST method 만 받는다.
def comment_like(request):
    pk = request.POST.get('pk', None)  # ajax 통신을 통해서 template에서 POST방식으로 전달
    comment = get_object_or_404(Comment, pk=pk)
    if hasattr(comment, 'like_user_set'):
        comment_like, comment_like_created = comment.like_set.get_or_create(user=request.user)
        if not comment_like_created:
            comment_like.delete()
            colortype = 'black'
        else:
            colortype = 'blue'

        context = {'like_count': comment.like_count,
                   'nickname': str(request.user),
                   'comment_like_created': comment_like_created,
                   'colortype': colortype,
                   }
        return HttpResponse(json.dumps(context), content_type="application/json")