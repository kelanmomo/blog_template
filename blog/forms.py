from django import forms
from .models import Post, Comment

class NewPostForm(forms.ModelForm):
    text_body = forms.CharField(
        widget=forms.Textarea(
            attrs={'row':11}
        ), 
        max_length=100000,
        help_text='文本最大支持字数为100000.'
        )
    class Meta:
        model = Post
        fields = ['title', 'text_body']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']