from audioop import reverse

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse,JsonResponse
from . models import *
import os

# Create your views here.
 
# 登陆视图
def mi_login(request):
    if request.method == 'POST':
        form = milogin(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=telephone, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    # return render(request,'index.html')
                    index_url = reverse('front_page:front_index')
                    return redirect(index_url)
            else:
                return HttpResponse('用户不存在')
        else:
          return HttpResponse('验证失败')
    else:
        return render(request, 'mi_login.html')


#注册视图
def mi_register(request):
    if request.method == 'GET':
        return render(request, 'mi_register.html')
    if request.method == 'POST':
        form = miregister(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            telephone = request.POST.get('telephone')
            if password1 != password2:
               return HttpResponse('两次密码不同')
            else:
                user = User.objects.create_user(telephone=telephone, username=username, password=password1)
                return render(request, 'mi_login.html',{'data':'已注册成功，请登陆。'})
        else:
            return HttpResponse('error')
        return HttpResponse('mixin')

# 显示个人信息
def user_information(request):
    if request.method == 'GET':
        user_id = request.user.uid
        user_object  =User.objects.filter(uid= user_id)[0]
        return render(request, 'information.html',{'user':user_object},)

# 个人信息修改
def update_information(request):
    if request.method == 'POST':
        user_id = request.user.uid
        user_object = User.objects.filter(uid=user_id)[0]
        username = request.POST.get('username')
        print(username)
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        if user_object.username != username and username.strip() != '':
            user_object.username = username
        if user_object.email != email and email.strip() != '':
            user_object.email = email
        # if password != None:
        #     user_object.set_password('password')
        user_object.save()
        return HttpResponse('成功')

#修改密码
def update_password(request):
    if request.method == 'POST':
        form = udpassword(request.POST)
        if form.is_valid():
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            print(old_password)
            print(new_password)
            user_id = request.user.uid
            user_object = User.objects.filter(uid=user_id)[0]
            if user_object.check_password(old_password):
                user_object.set_password(new_password)
                user_object.save()
                return render(request, 'mi_login.html')
            else:
                return HttpResponse('旧密码错误')
        else:
            return HttpResponse('未知错误')
    else:
        return HttpResponse('未知错误')