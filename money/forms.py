from django import forms
from .models import PiroMoney


class PiroMoneyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PiroMoneyForm, self).__init__(*args, **kwargs)
        self.fields['day'].widget.attrs['placeholder'] = '예) 2020-01-01'
        self.fields['user'].label = '이름'
        self.fields['type'].label = '종류'
        self.fields['day'].label = '날짜'

    class Meta:
        model = PiroMoney
        fields = ['user', 'type', 'day']
        help_texts = {
            'day': ('년도-월-일의 순서로 작성해주세요')
        }
