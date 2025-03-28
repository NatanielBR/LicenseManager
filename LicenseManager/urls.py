"""
URL configuration for LicenseManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api.views import LicenseViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
    ),
    public=False,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter(trailing_slash=False)
router.register('license', LicenseViewSet, basename='license')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include(router.urls))
]
