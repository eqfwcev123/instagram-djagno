from django.urls import path

from members.views import login_view, logout_view, naver_login

app_name = 'members'
urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='post-logout'),
    path('naver-login/', naver_login, name='naver-login')
]
