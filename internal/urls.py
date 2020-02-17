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
    path('qna/comment_like/', views.comment_like, name='comment_like'),
    path('address/', views.address_list, name='address_list'),
    path('address/create/', views.address_new, name='address_new'),
    path('address/edit/<int:pk>/', views.address_edit, name='address_edit'),
    path('address/delete/<int:pk>/', views.address_delete, name='address_delete'),
    path('checked/<int:pk>/', views.checked, name='checked'),
    path('checked_and_go/<int:pk>/<int:noti_pk>/', views.checked_and_go, name='checked_and_go'),
    # 내가 쓴 글 보기
    path('my_post/', views.my_post, name='my_post'),
    # qna 북마크
    path('bookmark_qna/<int:pk>/', views.create_bookmark_qna, name='create_bookmark_qna'),
    # 내가 북마크한 글 보기 / 삭제
    path('my_bookmark/', views.my_bookmark, name='my_bookmark'),
    path('my_bookmark/delete/delete/<int:pk>/',views.delete_bookmark, name = 'delete_bookmark')
]
