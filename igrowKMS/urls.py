"""igrowKMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
# from .import views
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from group import views
from sharing import views
from workshop import views
from rest_framework.authtoken import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.Indexpage),
    path('group/', include('group.urls')),
    path('sharing/', include('sharing.urls')),
    path('workshop/', include('workshop.urls')),
    path('', include('member.urls')),
    path('api-token-auth/', views.obtain_auth_token, name = 'api-token-auth'),
    path('login/', LoginView, name='login')
]
