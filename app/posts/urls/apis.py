from django.urls import path

from posts.apis import PostListCreateAPIView

urlpatterns = [
    path('', PostListCreateAPIView.as_view())
]
