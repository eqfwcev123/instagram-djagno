from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from members.forms import SignupForm, LoginForm
from members.models import User


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('posts:post-list')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'members/login.html', context)


def signup_view(request):
    email = request.POST['email']
    username = request.POST['username']
    name = request.POST['name']
    password = request.POST['password']

    # 인덱스 에서 사용자가 작성한 데이터가 여기로온다
    form = SignupForm(data=request.POST)
    if form.is_valid():  # True
        # form.clean()
        # user = User.objects.get(username=username)
        # login(request, user)
        return redirect('posts:post-list')


def logout_view(request):
    """
    로그인 되어있는지 확인하고 로그인 되어있을 경우 logout() 시키기.
    """
    logout(request)
    return redirect('members:login')
