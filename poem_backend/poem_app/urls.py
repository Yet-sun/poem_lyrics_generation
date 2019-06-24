# encoding: utf-8

'''
@author: sunyue
@contact: sunyue@mail.ynu.edu.cn
@software: pycharm
@file: urls.py
@time: 2019/6/16
@desc: 
'''

from django.urls import path
from poem_app import views

app_name = 'poem_app'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('index/',views.index,name='登陆'),
    path('register/',views.regist,name='注册'),
    path('log/', views.log, name='历史纪录' ),
    path('main/',views.main),
    path('get_valid_img.png/', views.get_valid_img),
    path('sendMsg/', views.sendMsg, name='sendMsg', ),
    path('get_rand_poem/', views.get_rand_poem, name='get_rand_poem', ),
    path('f_poem/', views.f_poem, name='f_poem', ),
    path('s_poem/', views.s_poem, name='s_poem', ),
    path('get_rand_sing/', views.get_rand_poem, name='get_rand_poem', ),

]

