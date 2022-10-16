from dataclasses import fields
from django import forms
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )
        labels = {
            'body': 'متنی ارسال کنید',
        }
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control','rows':1})
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control','rows':10})
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        labels = {
            'body': 'پاسخ',
        }
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control','rows':2})
        }