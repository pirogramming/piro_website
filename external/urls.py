from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('recruit/', views.recruit_list, name='recruit'),
    path('recruit/create/', views.recruit_new, name='recruit_new'),
    path('recruit/<int:pk>/', views.recruit_detail, name='recruit_detail'),
    path('recruit/<int:pk>/edit/', views.recruit_edit, name='recruit_edit'),
    path('recruit/<int:pk>/delete/', views.recruit_delete, name='recruit_delete'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/create/', views.portfolio_new, name='port_new'),
    path('portfolio/<int:pk>/edit/', views.port_edit, name='port_edit'),
    path('portfolio/<int:pk>/delete/', views.port_delete, name='port_delete'),
]

