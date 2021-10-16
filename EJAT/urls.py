"""EJAT URL Configuration

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
import debug_toolbar
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
import re

from django.views.static import serve

from EJAT.settings.dav import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('',include('public.urls')),
    path('register/', include('register.urls')),
    path('login/',include('login.urls')),
    path('contact/',include('contact.urls')),
    path('forget/', include('forget.urls')),
    path('reset/',include('reset.urls')),
    path('index/',include('index.urls')),
    path('category/',include('category.urls')),
    path('search/',include('search.urls')),
    path('single/',include('single.urls')),
    path('upload/', include('tinymce_upload.urls')),
    path('about_us/', include('about_us.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    re_path(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

]
