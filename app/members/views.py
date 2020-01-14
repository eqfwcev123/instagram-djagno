from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from members.forms import SignupForm, LoginForm
from members.models import User


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # is_valid() 이후에 self.cleaned_data 가 반환되었다
            form.login(request)
            return redirect('posts:post-list')
    else:
        # GET을 할때는 form 형식만 보내주면 되기 때문에 LoginForm 내부에 request.POST를 안넣어 줘도 된다.
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'members/login.html', context)


def signup_view(request):
    # POST 로 접근했을때
    if request.method == 'POST':
        form = SignupForm(request.POST)  # 사용자가 입력한 데이터가 옴
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:post-list')

    # GET 으로 로그인 했을때
    else:
        form = SignupForm()

        context = {
            'form': form,
        }
        return render(request, 'members/signup.html', context)


def logout_view(request):
    """
    로그인 되어있는지 확인하고 로그인 되어있을 경우 logout() 시키기.
    """
    logout(request)
    return redirect('members:login')
