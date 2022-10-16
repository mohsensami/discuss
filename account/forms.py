from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from account.models import Profile


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='نام کاربری', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}))
    email = forms.CharField(label='ایمیل', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('This username already exists')
        return username

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('password missmatch!')


class UserLoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))



class EditUserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ('avatar', 'age', 'bio', 'work_at', 'location')
        widgets = {
            'bio': forms.Textarea(attrs={'class':'form-control','rows':10}),
            'age': forms.NumberInput(attrs={'class':'form-control'}),
            'birth_date': forms.TextInput(attrs={'class':'form-control'}),
            'location': forms.TextInput(attrs={'class':'form-control'}),
            'work_at': forms.TextInput(attrs={'class':'form-control'}),
        }
