from django.shortcuts import render

def mainscreen(request):
    return render(request, 'main_intranet.html')
