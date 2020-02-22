import os

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from accounts.models import Bookmark
from infoboard.forms import InfoForm
from infoboard.models import Info, Files

@login_required
def list_info(request):
    info = Info.objects.all().order_by('-id')

    if request.method == 'POST':
        q = request.POST.get('q', '')  # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
        if q:  # q가 있으면
            info = info.filter(Q(title__icontains=q) | Q(text__icontains=q))# 제목에 q가 포함되어 있는 레코드만 필터링

        total_len = len(info)
        page = request.GET.get('page', 1)
        paginator = Paginator(info, 10)

        try:
            info = paginator.page(page)
        except PageNotAnInteger:
            info = paginator.page(1)
        except EmptyPage:
            info = paginator.page(paginator.num_pages)

        index = info.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        data = {
            'infos': info,
            'q': q,
            'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2
        }
        return render(request, 'infoboard/list_info.html', data)

    else:
        total_len = len(info)
        page = request.GET.get('page', 1)
        paginator = Paginator(info, 10)

        try:
            info = paginator.page(page)
        except PageNotAnInteger:
            info = paginator.page(1)
        except EmptyPage:
            info = paginator.page(paginator.num_pages)

        index = info.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        if index < 2:
            end_index = 5 - start_index
        else:
            end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range[start_index:end_index])

        data = {
            'infos':info,
            'page_range': page_range, 'total_len': total_len, 'max_index': max_index - 2
        }
        return render(request, 'infoboard/list_info.html', data)



@login_required
def detail_info(request, pk):
    info = Info.objects.get(pk=pk)
    file = info.files_set.all()

    data = {
        'info':info,
        'file':file,

    }
    return render(request, 'infoboard/detail_info.html', data)

@login_required
def create_info(request):
    if request.method == 'POST':
        form = InfoForm(request.POST, request.FILES)

        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            info.save()
            file_list = request.FILES.getlist('files')
            for item in file_list:
                files = Files.objects.create(info=info, file=item, filename = item.name)
                files.save()

            return redirect('infoboard:detail_info', info.pk)
        return redirect('infoboard:create_info')
    else:
        form = InfoForm()
        return render(request, 'infoboard/create_info.html', {'form':form})

@login_required
def update_info(request, pk):
    info = Info.objects.get(pk=pk)

    if request.method == 'POST' and request.user == info.user:
        form = InfoForm(request.POST, request.FILES)

        if form.is_valid():
            info.title = form.cleaned_data['title']
            info.text = form.cleaned_data['text']
            info.save()
            file_list = request.FILES.getlist('files')
            info.files_set.all().delete()
            for item in file_list:
                files = Files.objects.create(info=info, file=item, filename = item.name)
                files.save()
            return redirect('infoboard:detail_info', info.pk)
        return redirect('infoboard:update_info', info.pk)
    else:
        form = InfoForm(instance = info)
        return render(request, 'infoboard/create_info.html', {'form': form})

@login_required
def delete_info(request, pk):
    info = Info.objects.get(pk=pk)
    if request.user == info.user:
        temp = info.files_set.all()

        for i in temp:
            i.file.delete()

        info.delete()
    return redirect('infoboard:list_info')

@login_required
def download(request, pk, img_pk):
    file = get_object_or_404(Files, pk=img_pk)
    file_url = file.file.url[1:]
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_url)
            return response
    raise Http404

def create_bookmark_infoboard(request, pk):
    article = Info.objects.get(pk=pk)
    try:
        sample = Bookmark.objects.get(bookmark_title=article.title, pirouser=request.user, bookmark_type='infoboard')
    except:
        bookmark = Bookmark.objects.create(pirouser=request.user, bookmark_num=str(pk), bookmark_title=article.title, bookmark_type = 'infoboard')
        bookmark.save()

    return redirect('infoboard:detail_info', pk)