from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from members.models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # user에 사용자 계정이 저장된다.
        # print(user.is_superuser)
        # print(user.first_name)  # 이름
        # print(user.last_name)  # 성
        # print(user.email)  # 이메일
        # print(user.password)  # 비번(해쉬)
        # print(user.groups)  # 다른 그룹에 대한 Many To Many relationship
        # print(user.user_permissions)  # 다른 Permission 에 대한 Many To Many relationship
        # print(user.is_staff)  # admin site d에 접근할수 있는지 확인
        # print(user.is_active)  # 사용하고 있는 유저의 계정이 활동중인지 확인
        # print(user.is_superuser)  # 해당 유저가 모든 권한을 가지고 있는지 확인
        # print(user.last_login)  # 마지막 로그인 날짜
        # print(user.date_joined)  # 계정 이 생성된 날짜
        print(user)
        print(request.user.is_authenticated)
        # authenticate 는 사용자가 존재하는지만 확인
        if user:
            login(request, user)
            # 여기서 부터 set-cookie 에 관한 내용을 사용해야한다.
            return redirect('posts:post-list')
        else:
            # members의 urls.py 안에 있는 app_name:url패턴 이름
            return redirect('members:login')
    else:
        return render(request, 'members/login.html')


def signup_view(request):
    username = request.POST['username']
    email = request.POST['email']
    name = request.POST['name']
    password = request.POST['password']

    if User.objects.filter(username=username).exists():
        return HttpResponse("이미 사용중인 username/email 입니다")
    if User.objects.filter(email=email).exists():
        return HttpResponse("이미 사용중인 username/email 입니다")

    # 아이디가 같은데 비번이 다를경우 create_user() 를 할때 username 충돌이 난다
    # user = authenticate(username=username, password=password)
    # if user:
    #     return HttpResponse("이미 사용중인 username/email 입니다")
    # else:
    #     newuser = User.objects.create_user(username=username, email=email, name=name, password=password)
    #     login(request, newuser)
    #     return redirect('posts:post-list')

    user = User.objects.create_user(username=username, email=email, name=name, password=password)
    login(request, user)
    return redirect('posts:post-list')


def logout_view(request):
    """
    로그인 되어있는지 확인하고 로그인 되어있을 경우 logout() 시키기.
    """
    logout(request)
    return redirect('members:login')
