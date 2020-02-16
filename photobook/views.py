from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from photobook.forms import PhotobookForm
from photobook.models import Photobook, Images

@login_required
def list_book(request):
    photobook = Photobook.objects.all()
    data = {
        'photobooks':photobook,
    }
    return render(request, 'photobook/photo.html', data)

@login_required
def detail_book(request, pk):
    photobook = Photobook.objects.get(pk=pk)
    images = photobook.images_set.all()
    data = {
        'photobook':photobook,
        'images':images,
    }
    return render(request, 'photobook/photo_detail2.html', data)

@login_required
def create_book(request):
    if request.method == 'POST':
        form = PhotobookForm(request.POST, request.FILES)

        if form.is_valid():
            photobook = form.save(commit=False)
            photobook.user = request.user
            photobook.save()
            image_list = request.FILES.getlist('files')
            for item in image_list:
                images = Images.objects.create(photobook=photobook, image=item)
                images.save()

            return redirect('photobook:detail_book', photobook.pk)
        return redirect('photobook:create_book')
    else:
        form = PhotobookForm()
        return render(request, 'photobook/create_book.html', {'form':form})

@login_required
def update_book(request, pk):
    photobook = Photobook.objects.get(pk=pk)

    if request.method == 'POST':
        form = PhotobookForm(request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data)
            photobook.title = form.cleaned_data['title']
            photobook.text = form.cleaned_data['text']
            photobook.thumbnail = form.cleaned_data['thumbnail']
            photobook.save()
            image_list = request.FILES.getlist('files')
            photobook.images_set.all().delete()
            for item in image_list:
                images = Images.objects.create(photobook=photobook, image=item)
                images.save()
            return redirect('photobook:detail_book', photobook.pk)
        return redirect('photobook:update_book', photobook.pk)
    else:
        form = PhotobookForm(instance = photobook)
        return render(request, 'photobook/create_book.html', {'form': form})


@login_required
def delete_book(request, pk):
    photobook = Photobook.objects.get(pk=pk)
    temp = photobook.images_set.all()

    for i in temp:
        i.image.delete()

    photobook.delete()
    return redirect('photobook:list_book')