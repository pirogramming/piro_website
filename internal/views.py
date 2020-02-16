import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from internal.forms import QuestionForm, CommentForm, ReplyForm, InfoBookForm
from .models import Post, Comment, InfoBook


@login_required
def mainscreen(request):
    return render(request, 'main_intranet.html')

@login_required
def qna(request):
    post_list = Post.objects.all().order_by('-id')
    total_len = len(post_list)
    page = request.GET.get('page',1)
    paginator = Paginator(post_list, 10)

    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    index = questions.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    if index < 2:
        end_index = 5 - start_index
    else:
        end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range[start_index:end_index])

    return render(request, 'internal/qboard.html',{'questions': questions,'page_range':page_range, 'total_len':total_len, 'max_index':max_index-2})

@login_required
def q_new(request, post=None):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.tag = request.POST.get('tag')
            post.save()
            return redirect('intranet:q_detail', post.pk)
        else:
            return redirect("home:home")
    else:
        form = QuestionForm(instance=post)
        return render(request, 'internal/qcreate.html', {
            'form': form,
        })

def q_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        return q_new(request, post)
    else:
        return redirect('intranet:qna')

def q_delete(request, pk):
    post = Post.objects.get(id=pk)
    if request.user == post.author:
        post.delete()
        return redirect('intranet:qna')
    else:
        return redirect('intranet:qna')

@login_required
def q_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = post.comment_set.all()
    #comment = post.comment_set.all().order_by('-like_user_set')
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

@login_required
def q_by_tag(request):
    if request.method == 'POST':
        tag = request.POST.get('tag')
        if tag == 'all':
            return redirect('intranet:qna')
        else:
            post_list = Post.objects.all().filter(tag=tag).order_by('-id')
            total_len = len(post_list)
            page = request.GET.get('page',1)
            paginator = Paginator(post_list, 10)

            try:
                questions = paginator.page(page)
            except PageNotAnInteger:
                questions = paginator.page(1)
            except EmptyPage:
                questions = paginator.page(paginator.num_pages)

            index = questions.number - 1
            max_index = len(paginator.page_range)
            start_index = index - 2 if index >= 2 else 0
            if index < 2:
                end_index = 5 - start_index
            else:
                end_index = index + 3 if index <= max_index - 3 else max_index
            page_range = list(paginator.page_range[start_index:end_index])

            return render(request, 'internal/qboard.html',{'questions': questions, 'tag': tag, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index-2})
    else:
        return redirect('intranet:qna')

@login_required
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

@login_required
def comment_delete(request, pk, cmt_pk):
    post = Post.objects.get(pk=pk)
    comment = Comment.objects.get(pk=cmt_pk)
    comment.deleted = True
    comment.save()
    return redirect('intranet:q_detail', post.pk)

@login_required
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

def address_list(request):
    qs = InfoBook.objects.all().order_by('piro_no')
    return render(request, 'internal/address.html', {
        'address_list': qs,
    })

@login_required
def address_new(request, address=None):
    if request.method == 'POST':
        form = InfoBookForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.piro_no = request.user.piro_no
            address.save()
            return redirect("intranet:address_list")
        else:
            return redirect("intranet:address_list")
    else:
        form = InfoBookForm(instance=address)
        return render(request, 'internal/create_address.html', {
            'form': form,
        })

@login_required
def address_edit(request, pk):
    address = get_object_or_404(InfoBook, pk=pk)
    return address_new(request, address)

@login_required
def address_delete(request, pk):
    address = InfoBook.objects.get(id=pk)
    if request.user == address.user:
        address.delete()
        return redirect('intranet:address_list')
    else:
        return redirect('intranet:address_list')