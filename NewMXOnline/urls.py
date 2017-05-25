# _*_ coding: utf-8 _*_

"""NewMXOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

from users.views import RegisterCodeView, ResetCodeView, IndexView
from NewMXOnline.settings import MEDIA_ROOT
import xadmin

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^$', IndexView.as_view(), name='index'),

    #添加users include
    url(r'^users/', include('users.urls', namespace='users')),
    #添加CourseOrg include
    url(r'^org/', include('organizations.urls', namespace='orgs')),
    #添加Course include
    url(r'^course/', include('courses.urls', namespace='courses')),

    url(r'^captcha/', include('captcha.urls')),

    url(r'active/(?P<code>.*)/$', RegisterCodeView.as_view(), name='register_code'),

    url(r'reset/(?P<code>.*)/$', ResetCodeView.as_view(), name='reset_code'),

    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    #url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    url(r'^ueditor/',include('DjangoUeditor.urls' )),
]

#全局404 配置
handler404 = 'users.views.page_not_found'
#全局500配置
handler500 = 'users.views.page_error'

