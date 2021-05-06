"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_view

schema_view = get_schema_view(
    openapi.Info(
        title="Django Template Api Doc",
        default_version='v1',
    ),
)

urlpatterns = [
    path('', TemplateView.as_view(template_name="about.html")),
    path('admin/', admin.site.urls),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
