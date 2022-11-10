from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from account.models import Profile


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' Username'}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))
    password2 = forms.CharField(label='re Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 're Password'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This Email already exist')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('This Username already exist')
        return username

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('Password missmatch')


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))



class EditUserForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ('avatar', 'age', 'bio', 'work_at', 'location')
        labels = {
            'avatar': 'Avatar',
            'bio': 'Biography',
            'age': 'age',
            'birth_date': 'Birthdate',
            'location': 'location',
            'work_at': 'work at',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class':'form-control','rows':10}),
            'age': forms.NumberInput(attrs={'class':'form-control'}),
            'birth_date': forms.TextInput(attrs={'class':'form-control'}),
            'location': forms.TextInput(attrs={'class':'form-control'}),
            'work_at': forms.TextInput(attrs={'class':'form-control'}),
        }
