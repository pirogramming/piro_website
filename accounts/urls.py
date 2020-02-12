from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import UserCreateView, login, profile, profile_update, password_change

app_name = 'accounts'

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('login/', login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/update/', profile_update, name='profile_update'),
    path('password_change/', password_change, name='password_change'),
]

