from django import forms

from infoboard.models import Info


class InfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InfoForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['text'].label = '내용'
    
    class Meta:
        model = Info
        fields = ('title', 'text',)
