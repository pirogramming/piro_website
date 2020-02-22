from django.contrib import messages
from django.db.models import Max
from django.shortcuts import render, redirect,get_object_or_404
from .forms import NoticeForm, PortForm
from .models import Recruitment, Portfolio


def home(request):
    return render(request, 'main.html')

def portfolio(request):
    qs = Portfolio.objects.all()
    maxpiro = Portfolio.objects.aggregate(Max('pironumber'))
    if maxpiro.get("pironumber__max") == None:
        return redirect("home:port_new")
    maxno = maxpiro.get("pironumber__max") + 1
    return render(request, 'external/port_list.html',{
        'port_list': qs,
        'maxno': maxno,
        'range': range(1,maxno)
    })

def portfolio_new(request, port=None):
    if request.method == 'POST':
        form = PortForm(request.POST, request.FILES, instance=port)
        if form.is_valid():
            form.save()
            return redirect("home:portfolio")
        else:
            return redirect("home:home")
    else:
        form = PortForm(instance=port)
        return render(request, 'external/create_port.html', {
            'form': form,
        })

def port_edit(request, pk):
    port = get_object_or_404(Portfolio, pk=pk)
    return portfolio_new(request, port)

def port_delete(request, pk):
    if request.user.is_authenticated:
        if request.user.is_admin:
            port = Portfolio.objects.get(id=pk)
            port.delete()
            return redirect('home:portfolio')
        else:
            return redirect('home:home')
    else:
        return redirect('home:home')

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
            messages.error(request, '양식이 잘못되었습니다. 다시 시도해주세요.')
            return redirect("home:recruit")
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