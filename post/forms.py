from dataclasses import fields
from django import forms
from .models import Post


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control'})
        }
