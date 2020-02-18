from django.urls import path

from members.apis import AuthTokenAPIView

urlpatterns = [
    path('auth-token/', AuthTokenAPIView.as_view())
]
