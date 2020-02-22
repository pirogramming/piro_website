from django.urls import path

from money import views

app_name = 'money'

urlpatterns=[
    path('', views.check_money, name='check_money'),
]