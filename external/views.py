from django.shortcuts import render, redirect,get_object_or_404
from .forms import NoticeForm
from .models import Recruitment

def home(request):
    return render(request, 'main.html')

def portfolio(request):
    return render(request, 'external/port_list.html')

def recruit_list(request):
    qs = Recruitment.objects.all().order_by('-id')
    return render(request, 'external/recruit.html', {
        'notice_list': qs,
    })

def recruit_new(request, post=None):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home:recruit")
        else:
            return redirect("home:home")
    else:
        form = NoticeForm(instance=post)
        return render(request, 'external/create_recruit.html', {
            'form': form,
        })

def recruit_detail(request, pk):
    post = get_object_or_404(Recruitment, pk=pk)
    return render(request,'external/detail_recruit.html', {
        'post': post,
    })

def recruit_edit(request, pk):
    post = get_object_or_404(Recruitment, pk=pk)
    return recruit_new(request, post)

def recruit_delete(request, pk):

    if request.user.is_authenticated:
        if request.user.is_admin:
            post = Recruitment.objects.get(id=pk)
            post.delete()
            return redirect('home:recruit')
        else:
            return redirect('home:home')
    else:
        return redirect('home:home')