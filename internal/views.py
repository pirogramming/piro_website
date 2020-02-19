import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Max
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from accounts.models import Bookmark
from infoboard.models import Info
from internal.forms import QuestionForm, CommentForm, ReplyForm, InfoBookForm
from photobook.models import Photobook
from .models import Post, Comment, InfoBook, Notification


@login_required
def mainscreen(request):
    question_recent = Post.objects.all().order_by('-id')[:5]
    info_recent = Info.objects.all().order_by('-id')[:5]
    photo_recent = Photobook.objects.all().order_by('-id')[:3]
    notifications = Notification.objects.filter(to=request.user, checked=False)
    return render(request, 'main_intranet.html', {
        'question_recent': question_recent,
        'info_recent': info_recent,
        'photo_recent': photo_recent,
        'notifications': notifications,
    })


def checked(request, pk):
    notification_check = request.POST.get('checked')
    if notification_check:
        notification = Notification.objects.get(pk=pk)
        notification.delete()
    return redirect('intranet:mainscreen')


def checked_and_go(request, pk, noti_pk):
    notification = Notification.objects.get(pk=pk)
    notification.delete()
    return redirect('intranet:q_detail', noti_pk)


@login_required
def qna(request):
    post_list = Post.objects.all().order_by('-id')

    total_len = len(post_list)
    page = request.GET.get('page', 1)
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

    return render(request, 'internal/qboard.html',
                  {'questions': questions, 'page_range': page_range, 'total_len': total_len,
                   'max_index': max_index - 2})


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
    # comment = post.comment_set.all()
    comment = post.comment_set.all().order_by('-like_num')
    comment_no = comment.count()
    form = CommentForm()
    form2 = ReplyForm()
    path = request.META.get('HTTP_REFERER')
    return render(request, 'internal/qdetail.html', {
        'post': post,
        'comment': comment,
        'comment_no': comment_no,
        'form': form,
        'form2': form2,
        'path': path,
    })


@login_required
def q_by_tag(request):
    if request.method == 'POST':
        post_list = Post.objects.all()
        tag = request.POST.get('tag')
        q = request.POST.get('q', '')

        if tag == 'all':
            pass
        else:
            post_list = post_list.filter(tag=tag).order_by('-id')

        if q:
            post_list = post_list.filter(Q(title__icontains=q) | Q(body__icontains=q)).order_by('-id')

        total_len = len(post_list)
        page = request.GET.get('page', 1)
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

        return render(request, 'internal/qboard.html',
                      {'questions': questions, 'tag': tag, 'page_range': page_range, 'total_len': total_len,
                       'max_index': max_index - 2})
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
            if comment.author != comment.post.author:
                create_notification(comment.author, comment.post.author, '댓글', str(pk))
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
            if reply.author != reply.comment.author:
                create_notification(reply.author, reply.comment.author, '답글', str(post.pk))
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

        comment.like_num = comment.like_count
        comment.save()
        if request.user != comment.author:
            create_notification(request.user, comment.author, '좋아요', str(comment.post.pk))

        context = {'like_count': comment.like_count,
                   'nickname': str(request.user),
                   'comment_like_created': comment_like_created,
                   'colortype': colortype,
                   }
        return HttpResponse(json.dumps(context), content_type="application/json")


def create_notification(creator, to, notification_type, myid):
    notification = Notification.objects.create(
        creator=creator,
        to=to,
        notification_type=notification_type,
        myid=myid
    )
    notification.save()


def address_list(request):
    qs = InfoBook.objects.all().order_by('piro_no')
    maxpiro = InfoBook.objects.aggregate(Max('piro_no'))
    if maxpiro.get("piro_no__max") == None:
        return redirect("intranet:address_new")
    maxno = maxpiro.get("piro_no__max") + 1
    return render(request, 'internal/address.html', {
        'address_list': qs,
        'maxno': maxno,
        'range': range(1, maxno)
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
        if InfoBook.objects.filter(user=request.user).exists():
            messages.error(request, '이미 주소록에 등록되어 있습니다.')
            return redirect("intranet:address_list")
        elif request.user.is_admin:
            messages.error(request, '운영진은 주소록을 등록할 수 없습니다.')
            return redirect("intranet:mainscreen")
        else:
            form = InfoBookForm(instance=address)
            return render(request, 'internal/create_address.html', {
                'form': form,
            })


@login_required
def address_edit(request, pk):
    address = get_object_or_404(InfoBook, pk=pk)

    if request.method == 'POST':
        form = InfoBookForm(request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data)
            address.current_work = form.cleaned_data['current_work']
            address.history = form.cleaned_data['history']
            address.save()
            return redirect('intranet:address_list')
        return redirect('intranet:address_edit', pk)
    else:
        form = InfoBookForm(instance = address)
        return render(request, 'internal/create_address.html', {'form': form})


@login_required
def address_delete(request, pk):
    address = InfoBook.objects.get(id=pk)
    if request.user == address.user:
        address.delete()
        return redirect('intranet:address_list')
    else:
        return redirect('intranet:address_list')


# 내가 쓴 포스트 보기
def my_post(request):
    posts = Post.objects.filter(author=request.user)
    total_len = len(posts)
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    index = posts.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    if index < 2:
        end_index = 5 - start_index
    else:
        end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range[start_index:end_index])

    return render(request, 'internal/my_post.html', {'posts':posts, 'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2})

# qna 북마크
def create_bookmark_qna(request, pk):
    article = Post.objects.get(pk=pk)
    try:
        sample = Bookmark.objects.get(bookmark_title=article.title, pirouser=request.user, bookmark_type='qna')
    except:
        bookmark = Bookmark.objects.create(pirouser=request.user, bookmark_num=str(pk), bookmark_title=article.title, bookmark_type = 'qna')
        bookmark.save()

    return redirect('intranet:q_detail', pk)

# 내가 북마크한 글 보기
def my_bookmark(request):
    bookmarks = Bookmark.objects.filter(pirouser=request.user).order_by('-id')
    return render(request, 'internal/my_bookmark.html', {'bookmarks':bookmarks})

#북마크 삭제
def delete_bookmark(request, pk):
    bookmark = Bookmark.objects.get(pk = pk)
    bookmark.delete()
    return redirect('intranet:my_bookmark')
