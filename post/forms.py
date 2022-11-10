from dataclasses import fields
from django import forms
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )
        labels = {
            'body': '',
        }
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control','rows':1, 'cols': 60})
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        labels = {
            'body': 'Comment',
        }
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control','rows':10})
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        labels = {
            'body': 'Reply',
        }
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control','rows':2})
        }