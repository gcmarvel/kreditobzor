from django import forms


class CommentForm (forms.Form):
    author = forms.CharField(max_length=50, label='Имя')
    text = forms.CharField(max_length=4000, widget=forms.Textarea,label='Комментарий')
