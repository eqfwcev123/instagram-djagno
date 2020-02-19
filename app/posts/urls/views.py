from django.urls import path

from .. import views

app_name = 'posts'
urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('<int:pk>/like/', views.post_like, name='post-like'),
    path('create/', views.post_create, name='post-create'),
    path('<int:post_pk>/comments/create/', views.comment_create, name='post-comment'),
    path('<int:post_pk>/comments/', views.comment_list, name='post-comment-list'),
]
