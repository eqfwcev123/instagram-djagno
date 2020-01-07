### 유저 생성 방법
---
```python
from django.contrib.auth.models import User
user = User.objects.create_user(아이디, 이메일, 비번)
```

### 유저 인증
---
`authenticate(request=None, **credentials)` : authenticate 를 이용해서 사용자 인증을 한다.
**credentials 에 사용자의 `username`과 `password`를 넣어줘야한다. 장고는 해당 아이디와 비번을 authentication_backend 을 이용해서 검사를 하고
존재하는 사용자 이면 **해당 사용자를 반환한다. 존재하지 않을 경우 None을 반환한다.**

```python
from django.contrib.auth import authenticate
user = authenticate(username = '인증할 아이디', password = '인증할 비밀번호')
if user:
    pass
else:
    pass
```

### 장고에 있는 permission 종류
---
1. view : 파일 관람 권한
2. add : 데이터 추가 권한
3. change : 데이터 변경 권한
4. delete : 데이터 삭제 권한

사용자가 해당 권한을 가지고 있는지 알고 싶으면 ModelAdmin 클래스에서 제공하는 다음 메소드를 사용하면 된다.
`has_view_permission()`
`has_add_permission()`
`has_change_permission()`
`has_delete_permission()`

**모든 유저들은 두개의 ManyToManyField 를 가지고있다: groups, user_permissions**

### 사용자 기본 권한
---
startapp 을 이용해서 애플리케이션을 새로 만들게 되면 settingngs.py 에 있는 INSTALLED_APPS에 django.contrib.auth이 적혀있을것이다.
이 설정을 목적은 모든 장고 모델들 한테 기본 권한인 view, add, change, delete 를 부여하는 기능을 한다. 장고에서 각 모델들한테 권한을 부여 하면 
개발자들은 어떤 유저한테 어떠한 권한을 줄것인지를 정해서 알맞게 권한부여를 하면된다. python manage.py migrate 을 할때 해당 권한들이 각 모델들에
생성된다. 

### Groups(그룹)
---
django.contrib.auth.models.Group은 가장 기본적인 방법으로 사용자들을 분류하고 권한 부여를 할때 사용한다. 각 유저들은 개수제한 없이 몇개의 그룹에
속해있어도 상관 없다.

어떤 유저가 어떤 그룹에 속해있을 경우, 해당 유저는 그 그룹에대한 권한을 가지게 된다. 권한을 제외하고 그룹을 사용하게 되면 사용자들을 분류하는데 있어서 매우 편리하다.

### Authentication in web requests
---
장고는 세션과 미들웨어를 이용해서 request객체를 인증 시스템과 연결시킨다.
**사용자가 인증이 되어있을 경우 request.user 가 anonymous user 가 아닌 로그인 한 유저의 정보가 request.user 에 저장된다.**

사용자를 로그인 시키는 방법:
authenticate()를 이용해서 사용자를 인증시켰을 경우 다음 동작을 하고 싶을 것이다.
만약에 사용자를 session 과 연결 시키고 싶을 경우 login() 메소드를 사용하면 된다.
`login(request, user, backend=None)`: 인증된 사용자를 로그인 시키고 싶을 경우 login()메소드를 사용하면 된다.
**login() 메소드는 해당 사용자의 ID를 세션 프레임워크를 이용해서 세션에 저장을 시킨다**

authenticate() 와 login()을 사용하는 방법은 다음과 같다
```python
from django.contrib.auth import authenticate,login
def my_View(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username, password = password)
    if user is not None:
        login(request,user) # 사용자가 유효한 사용자일 경우 세션에 로그인 시킨다. 사용자의 정보가 세션에 저장이 된다.
        # Redirect to a success page
    else:
        # Return an invalid login error message
```

사용자를 로그아웃 시키는 방법:
`logout(request)`: django.contrib.auth.login()을 통해 로그인한 사용자를 로그아웃 시키기 위해서 django.contrib.auth.logout() 메소드를 사용한다.
```python
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page
```
`logout()` 함수는 사용자가 로그인이 되있지 않아도 에러를 발생시키지 않는다.
`logout()` 함수를 호출할 경우 서버 데이터베이스에 있는 유저의 세션 데이터가 삭제된다.

#### 비로그인 유저 접근 통제 방법
---
`requet.user.is_authenticated` : 인증이 된 사용자인지 확인
```python
from django.conf import settings
from django.shortcuts import redirect

def my_view(request):
    if not request.user.is_authenticated:
        return redirect(...)
```

다른 방법으로는 login required decorator를 사용하면 된다.
`login_required(redirect_field_name='next', login_url=None)`
첫번째 인자가 인증 성공시 우회할 url이다.
```python
from django.contrib.auth.decorators import login_required
@login_required
def my_view(request):
    pass
```     
@login_required는
1. 사용자가 로그인이 되있지 않을 경우, settings.LOGIN_URL로 우회한다. 
2. 사용자가 로그인 되어 있을경우, view 함수를 평소대로 호출한다.

비로그인 유저 접근을 통제하기 위해서 user.request.is_authenticated 혹은 @login_required를 사용했는데
추가적인 테스트를 사용해서 접근을 통제할 수 있다.   
```python
from django.shortcuts import redirect

def my_view(request):
    if not request.user.email.endswith('@example.com'):
        return redirect(...)
```

더 좋은 방법으로는 `user_pass_test()` shortcut 함수를 사용하면 된다.

`user_passes_test(test_func, =None, redirect_field_name='next')`
```python
from django.contrib.auth.decorators import user_passes_test

def email_check(user):
    return user.email.endswith('@example.com')
    
@user_passes_test(email_check)
def my_view(request):
    pass
```

`permission_required(perm, login_url='None',raise_exception=False)`



### Authentication views
---
