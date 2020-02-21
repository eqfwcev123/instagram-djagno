"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from members.views import signup_view
from posts.views import post_list_by_tag

# localhost:8000/api/ --> 이쪽으로 오는 경우 APIView를 사용
urlpatterns_apis = [
    path('members/', include('members.urls.apis')),
    path('posts/', include('posts.urls.apis'))
]

schema_view = get_schema_view(
    openapi.Info(
        title='WPS Instagram API',
        default_version='v1',
        contact=openapi.Contact(email="dohyeonee95@hotmail.com")
    ),
    public=True,
)

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('doc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('admin/', admin.site.urls),
    path('', signup_view, name='signup'),
    path('members/', include('members.urls.views')),
    path('posts/', include('posts.urls.views')),
    path('explore/tags/<str:tag>/', post_list_by_tag, name='post-list-by-tag'),
    path('api/', include(urlpatterns_apis))
]

# 이부분은 runserver 에서만 가능.
# staticfile

urlpatterns += static(
    # URL 앞부분이 /media/ 이면
    prefix=settings.MEDIA_URL,
    # document_root 위치에 나머지 path에 있는 파일을 리턴
    document_root=settings.MEDIA_ROOT
)
