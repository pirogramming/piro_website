from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('recruit/', views.recruit, name='recruit'),
    path('portfolio/', views.portfolio, name='portfolio'),
]