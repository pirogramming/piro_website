from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from .forms import SignUpForm, LoginForm, UserEditForm
from .models import PiroUser


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'accounts/signup_form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if user.is_admin:
                return HttpResponseRedirect(reverse('admin:index'))
            else:
                return redirect('home:home')
        else:
            try:
                user = PiroUser.objects.get(username=username)
                messages.error(request, '운영진의 인증이 완료되지 않은 계정입니다.')
                return redirect('accounts:login')
            except:
                messages.error(request,'아이디나 비밀번호를 확인해주세요.')
                return redirect('accounts:login')
    else:
        form = LoginForm()
    return render(request, 'accounts/login_form.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            done = form.save()
            return redirect("accounts:profile")
    else:
        profileform = UserEditForm(instance=request.user)
        forms = {'profileform': profileform}
        return render(request, 'accounts/profile_update.html', forms)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # Now an important bit is to call update_session_auth_hash() after you save the form. Otherwise the user’s auth session will be invalidated and she/he will have to log in again.
            messages.success(request, '비밀번호가 변경되었습니다. 변경된 비밀번호로 다시 로그인 해보세요.')
            logout(request)
            return redirect('accounts:login')
        else:
            messages.error(request, '오류를 수정해주세요.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {
        'form': form
    })