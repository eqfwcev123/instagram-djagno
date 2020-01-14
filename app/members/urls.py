from django.conf.urls import url
from django.urls import path

from members.views import login_view, signup_view, logout_view

app_name = 'members'
urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='post-logout'),
]
