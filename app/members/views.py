from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from members.forms import SignupForm, LoginForm
from members.models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(request.user.is_authenticated)
        # authenticate 는 사용자가 존재하는지만 확인
        if user:
            login(request, user)
            # 여기서 부터 set-cookie 에 관한 내용을 사용해야한다.
            return redirect('posts:post-list')
        else:
            # members의 urls.py 안에 있는 app_name:url패턴 이름
            return redirect('members:login')
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
        form.clean()
        user = User.objects.get(username=username)
        login(request, user)
    return redirect('posts:post-list')


def logout_view(request):
    """
    로그인 되어있는지 확인하고 로그인 되어있을 경우 logout() 시키기.
    """
    logout(request)
    return redirect('members:login')
