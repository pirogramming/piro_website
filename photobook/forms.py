from django import forms

from photobook.models import Photobook


class PhotobookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PhotobookForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '사진첩 이름'
        self.fields['text'].label = '사진첩 설명'
        self.fields['thumbnail'].label = '사진첩 썸네일 지정'
        
    class Meta:
        model = Photobook
        fields = ('title', 'text', 'thumbnail')