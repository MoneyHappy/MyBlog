# author:小欢子大人
# datetime:2018/8/1 15:11
#-*- coding:utf-8 -*-

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    '''登录验证'''
    username = forms.CharField(label='用户名',widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'请输入用户名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或者密码不正确,请检查后重新输入')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data



class RegisterForm(forms.Form):
    '''注册检查'''
    username = forms.CharField(label='用户名', min_length=2, max_length=15,
                               widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '请输入用户名，长度为2-15字符'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={
        'class':'form-control', 'placeholder': '请输入邮箱'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': '请输入密码'}))
    passwordAgain = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': '请再次输入密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_passwordAgain(self):
        password = self.cleaned_data['password']
        passwordAgain = self.cleaned_data['passwordAgain']
        if password != passwordAgain:
            raise forms.ValidationError('两次输入密码不一致')
        return password
