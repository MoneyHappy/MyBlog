# author:小欢子大人
# datetime:2018/8/1 14:58
#-*- coding:utf-8 -*-


from django.contrib import auth
from django.shortcuts import redirect, render, HttpResponse
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
import json
import re


def login(request):
    '''登录验证'''
    # username = request.POST.get('username')
    # password = request.POST.get('password')
    # user = auth.authenticate(request, username=username, password=password)
    # referer = request.META.get('HTTP_REFERER')
    # if user is not None:
    #     auth.login(request, user)
    #     return redirect(referer)
    # else:
    #     return render(request, 'error.html', {'message':'用户名或者密码不正确，请检查后重新登陆', 'redirect':referer})
    if request.method == 'POST':
        loginForms = LoginForm(request.POST)
        if loginForms.is_valid():
            user = loginForms.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from'))
    else:
        loginForms = LoginForm() #传给前端页面的表单

    content = {}
    content['loginForms'] = loginForms
    return render(request, 'login.html', content)



def logout(request):
    '''用户退出登录'''
    auth.logout(request)
    return redirect(request.GET.get('from'))



def register(request):
    '''用户注册'''
    if request.method == 'POST':
        registerForms = RegisterForm(request.POST)
        if registerForms.is_valid():
            username = registerForms.cleaned_data['username']
            email = registerForms.cleaned_data['email']
            password = registerForms.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            #用户登录
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from'))
            # user = User()
            # user.username = username
            # user.email = email
            # user.set_password(password) #密码有加密的
            # user.save()
    else:
        registerForms = RegisterForm()

    content = {}
    content['registerForms'] = registerForms
    return render(request, 'register.html', content)



def updateUserInfo(request):
    '''用户信息更新'''
    msg = {}
    if request.method == 'POST':
        print(request.POST)
        newUsername = request.POST.get('newUsername')
        newEmail = request.POST.get('newEmail')
        if User.objects.filter(username=newUsername).exclude(username=request.user.username):
            msg['repUsernameError'] = '此用户名已经存在'
        else:
            User.objects.filter(username=request.user.username).update(username=newUsername)
        if User.objects.filter(email=newEmail).exclude(email=request.user.email):
            msg['repEmailError'] = '此邮箱已经存在'
        else:
            User.objects.filter(email=request.user.email).update(email=newEmail)
    return HttpResponse(json.dumps(msg))



def smartSpeakerCommand(request):
    return render(request, 'smartSpeakerCommand.html')


def intelSmartSpeaker(request):
    'Intel智能音箱测试'
    command = []
    output = []
    if request.method == 'POST':
        print(request.POST)
        command.append(request.POST.get('command1'))
        output.append(request.POST.get('output1'))
        command.append(request.POST.get('command2'))
        output.append(request.POST.get('output2'))

        sendLi = list(zip(command, output))
        global sendStr
        sendStr = ''
        for i in sendLi:
            if i[0] != '' and i[1] != '':
                sendStr += (re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+--！，。？、~@#￥%……&*（）]", '', i[0]) + i[1]) + '*'
        sendStr = sendStr + '\0'
        print(sendStr)
    return HttpResponse(sendStr)
