from django import forms
from .models import Post, Response

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']