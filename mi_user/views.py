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
               pass
            else:
                user = User.objects.create_user(telephone=telephone, username=username, password=password1)
                return HttpResponse('注册成功')
        else:
            return HttpResponse('error')
        return HttpResponse('mixin')
