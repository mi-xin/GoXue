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
# 用户上传课程视图
def user_class_upload(request):
        print(1111111)
        if request.method == 'GET':
            # class_id = request.GET.get('class_id')
            # lesson = mi_class.objects.get(id=class_id)
            # print(lesson)
            return render(request, 'user_class_upload.html')
            # return HttpResponse('get')
        if request.method == 'POST':
            class_id = request.POST.get('class_id')
            print(class_id)
            if class_id is not None:
                class_boject = mi_class.objects.get(id=class_id)
                file = request.FILES.getlist('addfile')
            else:
                # 获取当前登陆的用户id
                create_user = request.user.uid
                # 获取当前用户对象
                user = User.objects.get(uid=create_user)
                # 前端获取数据
                file = request.FILES.getlist('myfile')
                title = request.POST.get('title')
                author = request.POST.get('author')
                introduce = request.POST.get('introduce')
                url= []
                name = []
                # 创建课程对象
                class_boject = mi_class(title=title,author=author,introduce=introduce,create_user=user)
                class_boject.save()
            # 遍历上传的文件，并保存
            for i in file:
                a=i.name
                i = mi_voide(file_name=a, file=i,class_name=class_boject)
                i.save()
                print(i)
                # url.append(i)
                # name.append(a)
            lesson = mi_class.objects.get(id=class_boject.id)
            # return render(request, 'user_class_upload.html',{'url':url,'name':name, 'b':b})
            # return HttpResponse('success')
            return render(request, 'class_admin.html', {'lesson': lesson})
# 返回课程相关的
def user_class_upload_id(request, class_id):
    if request.method == 'GET':
        class_id = class_id
        lesson = mi_class.objects.get(id=class_id)
        return render(request, 'class_admin.html', {'lesson': lesson})
    if request.method == 'POST':
        pass
 # 返回所有的课程
def user_class(request):
    if request.method == 'GET':
        user_now = request.user.uid
        user = User.objects.get(uid=user_now)
        user_class = user.create_user.all()
        allclass=[]
        for miclass in user_class:
            allclass.append(miclass)
        return render(request, 'user_class.html', {'allclass': allclass})
# 课程视频管理的方法
def class_admin(request):
    if request.is_ajax():
        if request.POST.get('sign') == 'update':
           # 前端获取数据
            class_id = request.POST.get('class_id')
            class_title = request.POST.get('class_title')
            class_introduce = request.POST.get('class_introduce')
            class_author = request.POST.get('class_author')
           #数据库查找对应id的课程
            class_object = mi_class.objects.get(id=class_id)
            if class_object.title != class_title:
                class_object.title = class_title
            if class_object.introduce != class_introduce:
                class_object.introduce = class_introduce
            if class_object.author != class_author:
                class_object.author =class_author
            class_object.save()
            response = JsonResponse({'class_title': class_object.title,
                             'class_introduce': class_object.introduce,
                             'class_author': class_object.author,
                            })
            return response
        elif request.POST.get('sign') == 'del':
            class_id = request.POST.get('class_id')
            del_id = request.POST.get('del_id')
            #  获取课程对象
            del_object = mi_voide.objects.get(id=del_id).delete()
            response = JsonResponse({'del_id':del_id})
            return response
        else:
            print(2222222222)
            return HttpResponse('操作有误')