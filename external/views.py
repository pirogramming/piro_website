from django.shortcuts import render


def home(request):
    return render(request, 'main.html')


def recruit(request):
    return render(request, 'external/recruit.html')


def portfolio(request):
    return render(request, 'external/port_list.html')