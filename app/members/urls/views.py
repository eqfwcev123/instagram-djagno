from django.urls import path

from .. import views

app_name = 'members'
urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='post-logout'),
    path('naver-login/', views.naver_login, name='naver-login')
]
