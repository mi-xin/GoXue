from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse, JsonResponse, FileResponse
import json
from . models import *
from mi_user.models import *
from django import forms
from django.core.paginator import Paginator , PageNotAnInteger,EmptyPage
# Create your views here.
import os
# 课程创建校验
class Upload_class(forms.Form):
    title = forms.CharField(label="课程名", error_messages={"required": "课程名必填"},)
    introduce = forms.CharField(label="简介", error_messages={"required": "简介必填"})
# 用户上传课程视图
def user_class_upload(request):
    if request.method == 'GET':
        return render(request, 'user_class_upload.html')
    if request.method == 'POST':
        # 文件类型类型的判断
        class_id = request.POST.get('class_id')
        if class_id is not None:
            sign = 'old'
            class_boject = mi_class.objects.get(id=class_id)
            chapter_name = request.POST.get('chapter_name')
            # 创建章节对象
            chapter_object = class_chapter(name=chapter_name, class_model=class_boject)
            chapter_object.save()
            files = request.FILES.getlist('addfile')
        else:
            sign = 'new'
            upload_form = Upload_class(request.POST)
            if upload_form.is_valid():
                # 获取当前登陆的用户id
                create_user = request.user.uid
                # 获取当前用户对象
                user = User.objects.get(uid=create_user)
                # 前端获取数据
                files = request.FILES.getlist('myfile')
                title = request.POST.get('title')
                author = request.POST.get('author')
                introduce = request.POST.get('introduce')
                chapter_name = request.POST.get('chapter_name')
                if request.FILES.getlist('img'):
                    imgfile = request.FILES.getlist('img')[0]
                    suffix = os.path.splittext(str(imgfile))[1]
                    suffix_list=['.png','.jpg']
                    if suffix in suffix_list:
                        class_boject = mi_class(title=title, author=author, introduce=introduce, create_user=user,
                                                class_image=imgfile)
                        class_boject.save()
                    else:
                        return redirect(reverse('mi_class:user_class_upload_id', args=(class_id,)),)
                else:
                    # 创建课程对象
                    class_boject = mi_class(title=title, author=author, introduce=introduce, create_user=user)
                    class_boject.save()
                    class_id = str(class_boject.id)
                    if chapter_name:
                        # 创建章节对象
                        chapter_object = class_chapter(name=chapter_name,class_model=class_boject)
                        chapter_object.save()
                    else:
                        lesson = mi_class.objects.get(id=class_boject.id)
                        return render(request, 'class_admin.html', {'lesson': lesson})
            else:
                # response = {"code": 1, "errors":'不知道为什么错',}
                # return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json,charset=utf-8")
                return render(request, "user_class_upload.html", {"code": 0, "errors": upload_form.errors})
        # 遍历上传的文件，并保存
        for i in files:
            bool =str(i).endswith(".mp4")
            if bool:
                name = i.name
                voide = mi_voide(file_name=name, file=i, chapter_name=chapter_object)
                voide.save()
            else:
                chapter_object.delete()
                context = {
                    'code':0,
                    'error':'文件类型错误，只支持上传mp4',
                }
                return redirect(reverse('mi_class:user_class_upload_id', args=(class_id,)),context)
        # 课程对象
        lesson = mi_class.objects.get(id=class_boject.id)
        # 章节对象
        chapter_lists = []
        chapter_objects = class_chapter.objects.filter(class_model=lesson)
        for i in chapter_objects:
            video_objects = i.class_chapter.all()
            chapter_lists.append({
                'chapter_object': i,
                'video_objects': video_objects,
            })
        return redirect(reverse('mi_class:user_class_upload_id', args=(lesson.id,)),{'lesson': lesson,'chapter_lists':chapter_lists})
# 返回课程相关的
def user_class_upload_id(request, class_id):
    if request.method == 'GET':
        # 课程对象
        class_id = class_id
        lesson = mi_class.objects.get(id=class_id)
        # 章节对象
        chapter_lists = []
        chapter_objects = class_chapter.objects.filter(class_model=lesson)
        for i in chapter_objects:
            video_objects = i.class_chapter.all()
            chapter_lists.append({
                'chapter_object':i,
                'video_objects':video_objects,
            })
        # 返回课程相关资料
        data_list = []
        try:
            data_object = CourseMaterials.objects.filter(data_id=lesson)
            for i in data_object:
                data_list.append(i)
        except:
            data_list= []
        return render(request, 'class_admin.html', {'lesson': lesson,'chapter_lists':chapter_lists,'data_list':data_list})
    if request.method == 'POST':
        pass
# 课程的展示
def user_class(request,sign):
    if request.method == 'GET':
        user_now = request.user.uid
        user = User.objects.get(uid=user_now,is_active=1)
        global user_class
        allclass = []
        if sign == 'all':
            user_class = user.create_user.filter(is_active=1)
        if sign =='yes':
            user_class = user.create_user.filter(is_release=1,is_active=1)
        if sign =='no':
            user_class = user.create_user.filter(is_release=0,is_active=1)
        paginator = Paginator(user_class, 2, 0)
        try:
            # 获取index的值，如果没有，则设置使用默认值1
            num = request.GET.get('index', '1')
            # 获取第几页
            number = paginator.page(num)
        except PageNotAnInteger:
            # 如果输入的页码数不是整数，那么显示第一页数据
            number = paginator.page(1)
        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        return render(request, 'user_class.html', {'page':number,'paginator':paginator,'sign':sign})
    else:
        return HttpResponse('出现问题了')
# 课程的删除与发布的管理
def lesson_admin(request):
    if request.is_ajax():
        if request.POST.get('sign') == 'del':
            # 前端获取数据
            id = request.POST.get('id')
            class_object = mi_class.objects.get(id=id)
            class_object.is_active = False
            class_object.save()
            return JsonResponse({'code':1})
        elif request.POST.get('sign') == 'release':
            # 前端获取数据
            id = request.POST.get('id')
            class_object = mi_class.objects.get(id=id)
            class_object.is_release = True
            class_object.save()
            return JsonResponse({'code':1})
        else:
            return JsonResponse({'code':0})
    else:
        return HttpResponse('操作有误')
# 课程视频管理(课程信息的修改/视频的增加删除/章节的删除/章节信息的修改及章节的增加)
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
            response = JsonResponse({'code': 1})
            return response
        elif request.POST.get('sign') =='del_chapter':
            chapter_id = request.POST.get('del_id')
            chapter_object = class_chapter.objects.get(id=chapter_id)
            chapter_object.delete()
            print(chapter_object)
            response = JsonResponse({'code': 1})
            return response
        else:
            return HttpResponse('操作有误')
    else:
        # 前端获取要修改的章节名称/文件
        name = request.POST.get('updata_chapter_name')
        file = request.FILES.getlist('chapter_file')
        chapter_id = request.POST.get('chapter_id')
        # 获取章节对象
        chapter_object = class_chapter.objects.get(id=chapter_id)
        # 修改章节的名称
        if name and name != chapter_object.name:
            chapter_object.name = name
            chapter_object.save()
        for i in file:
            name = i.name
            voide = mi_voide(file_name=name, file=i, chapter_name=chapter_object)
            voide.save()
        lesson_id = chapter_object.class_model_id
        # 课程对象
        lesson = mi_class.objects.get(id=lesson_id)
        # 章节对象
        chapter_lists = []
        chapter_objects = class_chapter.objects.filter(class_model=lesson)
        for i in chapter_objects:
            video_objects = i.class_chapter.all()
            chapter_lists.append({
                'chapter_object': i,
                'video_objects': video_objects,
            })
        return redirect(reverse('mi_class:user_class_upload_id', args=(lesson.id,)),{'lesson': lesson, 'chapter_lists': chapter_lists})

# 视频播放面的方法
def video_play(request,class_id):
    if request.method == 'GET':
        class_id = class_id
        lesson = mi_class.objects.get(id=class_id)
        # 章节对象
        chapter_lists = []
        chapter_objects = class_chapter.objects.filter(class_model=lesson)
        for i in chapter_objects:
            video_objects = i.class_chapter.all()
            chapter_lists.append({
                'chapter_object': i,
                'video_objects': video_objects,
            })
        # 获取该文章的评论
        comments = lesson.lessonComment.all().order_by('-id')
        count = comments.count()
        paginator = Paginator(comments, 2, 0)
        try:
            # GET请求方式，get()获取指定Key值所对应的value值
            # 获取index的值，如果没有，则设置使用默认值1
            num = request.GET.get('index', '1')
            number = paginator.page(num)
        except PageNotAnInteger:
            # 如果输入的页码数不是整数，那么显示第一页数据
            number = paginator.page(1)
        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        return render(request, 'play.html', {'lesson': lesson,'chapter_lists': chapter_lists,'page':number,'paginator':paginator,})
    if request.method == 'POST':
        pass
# 切换视频播视频的方法
def switch_play(request):
    if request.method == 'POST':
        play_id = request.POST.get('play_id')
        play_object = mi_voide.objects.get(id=play_id)
        play_src = play_object.file.url
        response = JsonResponse({'play_src': play_src,})
        return response

# 课程评论功能
def comment(request):
    if request.is_ajax():
        if request.method == 'POST':
            comment = request.POST.get('comment')
            lesson_id = request.POST.get('lesson_id')
            try:
                lesson = mi_class.objects.get(id = lesson_id)
            except:
                return HttpResponse('没有课程对象')
            user = request.user
            user_name = user.username
            headImgUrl = user.userotherinformtion.headImg.url
            comment_object = Comment(lesson=lesson,user=user,content=comment)
            comment_object.save()
            data = comment_object.data
            return JsonResponse({'code':1, 'comment':comment,'user_name':user_name,'data':data,'headImgUrl':headImgUrl})
        else:
            return HttpResponse('失败了')
# 课程资料文件下载
def download(request):
    if request.is_ajax():
        print(11111)
        fileid = request.POST.get('id')
        print(id)
        print(2222)
        file_object = CourseMaterials.objects.get(id= fileid)
        print(file_object)
        file = open(file_object.file.path, 'rb')
        response = FileResponse(file)
        print(88)
        print(response)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="models.py"'
        # return JsonResponse({'code':1,'response':response})
        return response
    else:
        return JsonResponse({'code':0})
# 课程资料的上传及删除
def admin_data(request):
    if request.is_ajax():
        if request.POST.get('sign') == 'add':
            id = request.POST.get('id')
            lesson_boject = mi_class.objects.get(id=id)
            try:
                files = request.FILES.get('data')
                print(files)
            except:
                pass
            data_object = CourseMaterials(file=files, name=files.name, data=lesson_boject)
            data_object.save()
            return JsonResponse({'code':1})
        else:
            return JsonResponse({'code':0})