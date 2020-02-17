from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from infoboard import views

app_name = 'infoboard'

urlpatterns = [
    path('<int:pk>/', views.detail_info, name='detail_info'),
    path('', views.list_info, name="list_info"),
    path('create/', views.create_info, name="create_info"),
    path('<int:pk>/update/', views.update_info, name="update_info"),
    path('<int:pk>/delete/', views.delete_info, name="delete_info"),
    path('<int:pk>/<int:img_pk>/download/', views.download, name="download"),                   ########### 다운로드 ############
]

if settings.DEBUG:
    urlpatterns += static(settings.INFO_MEDIA_URL, document_root=settings.MEDIA_ROOT)