from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import PiroUser



class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'

        self.fields['password1'].help_text = "8자 이상, 영문 숫자 특수문자 중 둘 이상을 섞어주세요"
        self.fields['password2'].help_text = "비밀번호를 한번 더 입력해주세요"

        self.fields['name'].widget.attrs['placeholder'] = '예) 홍길동'
        self.fields['phone_no'].widget.attrs['placeholder'] = '예) 010-1234-5678'
        self.fields['piro_no'].widget.attrs['placeholder'] = '예) 12'
        self.fields['github'].widget.attrs['placeholder'] = '예) https://github.com/pirogramming'

    class Meta:
        model = PiroUser
        fields = ['email', 'name', 'username', 'phone_no', 'piro_no', 'img_profile', 'github']

        help_texts = {
            'email': ('이메일 형식에 맞게 적어주세요'),
            'phone_no': ('"-" 를 포함해서 입력해주세요'),
            'piro_no': ('숫자만 입력 가능합니다.'),
            'img_profile': ('25MB이하 파일만 가능합니다'),
            'github': ('깃허브 링크를 입력해주세요.'),
        }

    def saved(self):
        user = super().save()
        PiroUser.objects.create(
            user=user,
            email=self.cleaned_data['email'],
            name=self.cleaned_data['name'],
            username=self.cleaned_data['username'],
            phone_no=self.cleaned_data['phone_no'],
            piro_no=self.cleaned_data['piro_no'],
            img_profile=self.cleaned_data['img_profile'],
            github=self.cleaned_data['github']
        )
        return user


class LoginForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '아이디/ 닉네임'
        self.fields['password'].label = '비밀번호'

    class Meta:
        model = PiroUser
        widgets = {'password': forms.PasswordInput}
        fields = ['username', 'password']


class UserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PiroUser
        fields = ['email', 'username', 'phone_no', 'img_profile', 'github']

        help_texts = {
            'email': ('이메일 형식에 맞게 적어주세요'),
            'nickname': ('다섯자 이하로 입력하세요'),
            'img_profile': ('25MB이하 파일만 가능합니다'),
            'github': ('깃허브 링크를 입력해주세요.'),
        }