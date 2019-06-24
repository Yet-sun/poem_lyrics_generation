"""poem_backend URL Configuration

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
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('poem_app/', include('poem_app.urls')),
    path('admin/', admin.site.urls),
    # path('captcha/', include('captcha.urls')),
]


# from django.urls import path
# from poem_app import views
# app_name = 'poem_app'
# urlpatterns = [
#     # path('admin/', admin.site.urls),
#     path('index/',views.index,name='登陆'),
#     path('register/',views.regist,name='注册'),
#     path('main/',views.main),
#     path('get_valid_img.png/', views.get_valid_img),
#     # url(r'^send_message$', views.send_message, name='send_message'),
#     path('sendMsg/', views.sendMsg, name='sendMsg', ),
#     # path('s/', views.s, name='s', )
# ]