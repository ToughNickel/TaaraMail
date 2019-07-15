"""TaaraMail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.views.decorators.cache import never_cache

from mail_sender import views
from django.conf import settings
from django.conf.urls.static import static
from ckeditor_uploader import views as uploader_views
from django_summernote import urls

urlpatterns = [
    # Invoke the home view in the mail_sender app by default
    url(r'^$', views.home, name='home'),
    url(r'^mail_sender/', include('mail_sender.urls', namespace='mail_sender')),
    url(r'^ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(uploader_views.browse), name='ckeditor_browse'),
    url(r'^summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
