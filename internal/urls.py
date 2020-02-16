from django.urls import path
from . import views

app_name = 'intranet'

urlpatterns = [
    path('', views.mainscreen, name='mainscreen'),
    path('qna/', views.qna, name='qna'),
    path('qna/create/', views.q_new, name='q_new'),
    path('qna/by_tag/', views.q_by_tag, name='q_by_tag'),
    path('qna/<int:pk>/', views.q_detail, name='q_detail'),
    path('qna/edit/<int:pk>/', views.q_edit, name='q_edit'),
    path('qna/delete/<int:pk>/', views.q_delete, name='q_delete'),
    path('qna/comment/<int:pk>/', views.comment_create, name='comment_create'),
    path('qna/comment/delete/<int:pk>/<int:cmt_pk>/', views.comment_delete, name='comment_delete'),
    path('qna/reply/<int:pk>/<int:cmt_pk>/', views.reply_create, name='reply_create'),
    path('qna/comment_like/', views.comment_like, name= 'comment_like'),
]

