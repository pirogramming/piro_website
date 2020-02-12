from django import forms
from .models import Recruitment

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Recruitment
        fields = ['title', 'content', 'img']