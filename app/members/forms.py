from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render

from members.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='username', widget=forms.TextInput(
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

    def login(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        login(request, user)

    def clean(self):

        # Form.clean 에서는 cleaned_data 에 접근할 수 있다.
        # clean_data 에는 이 Form이 가진 모든 필드들에서 리턴된 데이터가 key:value 형식으로 저장되어 있다
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username,password=password)
        if not user:
            raise ValidationError("username 또는 password 가 이미 존재합니다")
        return self.cleaned_data


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
