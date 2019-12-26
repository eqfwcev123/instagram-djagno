from django.conf.urls import url
from django.urls import path

from members.views import login_view

app_name = 'members'
urlpatterns = [
    path('', login_view, name='login'),
]
