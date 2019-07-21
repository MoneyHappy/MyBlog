# author:小欢子大人
# datetime:2018/7/10 15:57
#-*- coding:utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogHome),
    path('<int:blog_id>', views.blogDetail, name='blogDetail'),
    path('type/<int:type_id>', views.blogWithType, name='blogWithType'),
]
