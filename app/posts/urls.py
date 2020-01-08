from django.urls import path

from posts.views import post_list, post_like, post_create

app_name = 'posts'
urlpatterns = [
    path('', post_list, name='post-list'),
    path('<int:pk>/like/', post_like, name='post-like'),
    path('create/', post_create, name='post-create'),
]
