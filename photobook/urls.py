from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from photobook import views

app_name = 'photobook'

urlpatterns = [
    path('<int:pk>/', views.detail_book, name='detail_book'),
    path('', views.list_book, name="list_book"),
    path('create/', views.create_book, name="create_book"),
    path('<int:pk>/update/', views.update_book, name="update_book"),
    path('<int:pk>/delete/', views.delete_book, name="delete_book"),
]

if settings.DEBUG:
    urlpatterns += static(settings.PHOTOBOOK_MEDIA_URL, document_root=settings.MEDIA_ROOT)