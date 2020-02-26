from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse,JsonResponse
from . models import *
from mi_user.models import *

# Create your views here.
import os
# 用户上传课程视图
def user_class_upload(request):
    if request.method == 'GET':
        # class_id = request.GET.get('class_id')
        # lesson = mi_class.objects.get(id=class_id)
        return render(request, 'user_class_upload.html')
        # return HttpResponse('get')
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
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
            imgfile = request.FILES.getlist('img')[0]
            print(imgfile)
            url = []
            name = []
            # 创建课程对象
            class_boject = mi_class(title=title, author=author, introduce=introduce, create_user=user,
                                    class_image=imgfile)
            class_boject.save()
        # 遍历上传的文件，并保存
        for i in file:
            a = i.name
            i = mi_voide(file_name=a, file=i, class_name=class_boject)
            i.save()
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
def user_class(request,sign):
    if request.method == 'GET':
        print(sign)
        user_now = request.user.uid
        user = User.objects.get(uid=user_now)
        global user_class
        allclass = []
        if sign == 'all':
            print(1111)
            user_class = user.create_user.all()
            print(user_class)
        if sign =='yes':
            print(222)
            user_class = user.create_user.filter(is_release=1)
        if sign =='no':
            print(333)
            user_class = user.create_user.filter(is_release=0)
        for i in user_class:
            allclass.append(i)
            print(8888)
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
            # 数据库查找对应id的课程
            class_object = mi_class.objects.get(id=class_id)
            if class_object.title != class_title:
                class_object.title = class_title
            if class_object.introduce != class_introduce:
                class_object.introduce = class_introduce
            if class_object.author != class_author:
                class_object.author = class_author
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
            response = JsonResponse({'del_id': del_id})
            return response
        else:
            return HttpResponse('操作有误')

# 视频播放面的方法
def video_play(request,class_id):
    if request.method == 'GET':
        class_id = class_id
        lesson = mi_class.objects.get(id=class_id)
        return render(request, 'play.html', {'lesson': lesson})
    if request.method == 'POST':
        pass
# 切换视频播视频的方法
def switch_play(request):
    if request.method == 'POST':
        play_id = request.POST.get('play_id')
        print(play_id)
        play_object = mi_voide.objects.get(id=play_id)
        print(play_object)
        play_src = play_object.file.url
        response = JsonResponse({'play_src': play_src,})
        return response