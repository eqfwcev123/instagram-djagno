from django import forms
from django.contrib.auth import authenticate
from django.http import HttpResponse

from members.models import User


class LoginForm(forms.Form):
    usernmae = forms.CharField(label='username', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '아이디'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '비밀번호'
        }
    ))


class SignupForm(forms.Form):
    name = forms.CharField(max_length=250, widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    username = forms.CharField(max_length=250, widget=forms.TextInput())
    password = forms.CharField(max_length=250, widget=forms.PasswordInput())

    def clean(self):
        # 사용자가 보낸 데이터
        cleaned_data = super(SignupForm, self).clean()
        username_passed = cleaned_data.get("username")
        email_passed = cleaned_data.get("email")
        print('클린 데이터는: ', cleaned_data)
        print('유전네임 패스는: ', username_passed)
        print('이메일 패스는: ', email_passed)
        if username_passed in User.objects.filter(username=username_passed):
            raise forms.ValidationError("이미 사용중인 username입니다")
        if email_passed in User.objects.filter(email=email_passed):
            raise forms.ValidationError("이미 사용중인 username입니다")
        User.objects.create(email=cleaned_data.get("email"), username=cleaned_data.get('username'),
                            password=cleaned_data.get('password'), name=cleaned_data.get('name'))
