from django.urls import path
from . import views

app_name = 'intranet'

urlpatterns = [
    path('', views.mainscreen, name='mainscreen'),
    path('qna/', views.qna, name='qna'),
    path('qna/create/', views.q_new, name='q_new'),
    path('qna/<int:pk>/', views.q_detail, name='q_detail'),
    path('qna/comment/<int:pk>/', views.comment_create, name='comment_create'),
    path('qna/reply/<int:pk>/<int:cmt_pk>/', views.reply_create, name='reply_create'),
    path('qna/comment_like/', views.comment_like, name= 'comment_like'),
]

