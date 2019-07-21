# author:小欢子大人
# datetime:2018/7/31 20:08
#-*- coding:utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('submitComment/', views.submitComment),
    path('removeComment/', views.removeComment),
]
