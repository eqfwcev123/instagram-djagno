from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.forms import formset_factory
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

    def clean(self):
        # Form.clean 에서는 cleaned_data 에 접근할 수 있다.
        # clean_data 에는 이 Form이 가진 모든 필드들에서 리턴된 데이터가 key:value 형식으로 저장되어 있다
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("username 또는 password 가 옳바르지 않습니다")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        login(request, user)


class SignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이메일',
            }
        )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이름',
            }
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '사용자명',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호',
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('이미 사용중인 username입니다')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('이미 사용중인 email입니다')
        return email

    # 유효한 이메일 과 아이디인지 확인한다
    # form.non_field_errors 는 에러가 정확히 어떤 필드에서 나는지 모르기 때문에
    # 모든 에러를 가지고 있다. 하지만 만약에 에러를 필드별로 나누게 되면
    # 해당 필드가 어떤 에러를 가지고있는지 알 수 있기 때문에 non_field_error 를 사용하면 안된다.
    # def clean(self):
    #     username = self.cleaned_data['username']
    #     email = self.cleaned_data['email']
    #
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError("이미 사용중인 username입니다")
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("이미 사용중인 username입니다")
    #     return self.cleaned_data

    def save(self):
        """
        Form으로 전달받은 데이터를 사용해서
        새로운 User를 생성하고 리턴
        """
        return User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            name=self.cleaned_data['name'],
        )
