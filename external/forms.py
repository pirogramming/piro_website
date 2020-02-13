from django import forms
from .models import Recruitment, Portfolio


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Recruitment
        fields = ['title', 'content', 'img']

class PortForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = '290 X 290의 정사각형 이미지를 삽입해주세요.'

    class Meta:
        model = Portfolio
        fields = '__all__'