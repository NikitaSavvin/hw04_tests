from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('group', 'text',)
        labels = {
            'group': ('Группа'),
            'text': ('Текст'),
        }
        help_texts = {
            'text': 'Введите текст ',
            'group': 'Укажите группу',
        }

    def clean_subject(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError("Вы должны заполнить это поле")
        return data
