import urllib
from datetime import datetime

import requests
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

    login_base_url = 'https://nid.naver.com/oauth2.0/authorize'
    login_params = {
        'response_type': 'code',
        'client_id': 'DTs2e7pHYcuPAmfCI7Kg',
        'redirect_url': 'http://localhost:8000/members/naver-login/',
        'state': 'RANDOM_STATE',
    }
    login_url = '{base}?{params}'.format(
        base=login_base_url,
        params='&'.join([f'{key}={value}' for key, value in login_params.items()])
    )
    print('유알엘은 : ', login_url)

    context = {
        'form': form,
        'login_url': login_url,
    }
    return render(request, 'members/login.html', context)


def signup_view(request):
    # POST 로 접근했을때
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:post-list')
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


def naver_login(request):
    # GET Parameter로 전달된 code값을 사용해서
    # 네이버 API의 php 샘플 코드를 보고
    # token_url을 생성
    # print(token_url)
    login_base_url = "https://nid.naver.com/oauth2.0/token"
    login_params = {
        'grant_type': 'authorization_code',
        'client_id': 'DTs2e7pHYcuPAmfCI7Kg',
        'client_secret': '8ZtHtnt7B9',
        'redirect_url': 'http://localhost:8000/members/naver-login/',
        'code': request.GET['code'],
        'state': request.GET['state'],
    }

    # ClientID는 공개값
    # 네이버 로그인 버튼 <a href="....client_id=<Client_Id>9"
    # ClientSecret는 비공개 값

    token_url = '{base}?{params}'.format(
        base=login_base_url,
        params='&'.join([f'{key}={value}' for key, value in login_params.items()])
    )

    print('토큰 유알엘은: ', token_url)
    # resposne 에 token_url 에 대한 응답이 저장되어 있다. response 에 저장되는 것은 response status이다
    response = requests.get(token_url)
    print(response)
    print('상태: ', response.status_code)
    access_token = response.json()['access_token']
    me_header = {
        'Authorization': f"Bearer {access_token}"
    }
    me_url = "https://openapi.naver.com/v1/nid/me"
    me_response = requests.get(me_url, headers=me_header)
    me_response_data = me_response.json()
    print(me_response_data)
    unique_id = me_response_data['response']['id']
    print(unique_id)

    naver_username = f'n_{unique_id}'
    if not User.objects.filter(username=naver_username).exists():
        user = User.objects.create_user(username=naver_username)
    else:
        user = User.objects.get(username=naver_username)
    login(request, user)
    return redirect('posts:post-list')
