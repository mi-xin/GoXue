from audioop import reverse

from django.contrib.auth import authenticate, login,logout
from django import forms
from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse,JsonResponse
from . models import *
from mi_class.models import *
from django.core.paginator import Paginator , PageNotAnInteger,EmptyPage
from django.core.mail import send_mail
import string
import random
from GoXue.settings import EMAIL_FROM
# Create your views here.
# 登陆注册校验表单
class miregister(forms.Form):
    username = forms.CharField(max_length=8, required=True)
    password1 = forms.CharField(max_length=30, required=True)
    password2 = forms.CharField(max_length=30, required=True)
    telephone = forms.CharField(max_length=11, required=True)
    # email = forms.EmailField()
class milogin(forms.Form):
    password = forms.CharField(max_length=30, required=True)
    telephone = forms.CharField(max_length=11, required=True)
# 修改密码校验
class udpassword(forms.Form):
    old_password = forms.CharField(max_length=30, required=True)
    new_password = forms.CharField(max_length=30, required=True)
# 重置密码邮箱校验
class forgetpw(forms.Form):
    email = forms.EmailField(required=True)
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
                    index_url = reverse('front_page:front_index')
                    return redirect(index_url)
            else:
                return render(request, 'mi_login.html', {'code': 0, 'error': '用户/密码错误'})
        else:
          return render(request, 'mi_login.html', {'code': 0, 'error': '手机号/密码不能为空'})
    else:
        return render(request, 'mi_login.html')
#注册视图
def mi_register(request):
    if request.method == 'GET':
        return render(request, 'mi_register.html')
    if request.method == 'POST':
        flag = False
        form = miregister(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            telephone = request.POST.get('telephone')
            # email = request.POST.get('email')
            try:
                flag = User.objects.get(telephone=telephone)
                flag = True
            except:
                flag = False
            if password1 != password2:
               return render(request, 'mi_register.html', {'error': '两次密码不同'})
            elif flag:
                return render(request, 'mi_register.html', {'code': 200, 'data': '该手机号已被注册'})
            else:
                user = User.objects.create_user(telephone=telephone, username=username, password=password1,)
                userInformation = UserOtherInformtion(user=user)
                userInformation.save()
                return render(request, 'mi_login.html',{'code':200,'data':'已注册成功，请登陆。'})
        else:
            return render(request, 'mi_register.html', {'error': '信息不能为空/用户名不能超过8个字符'})
        return HttpResponse('mixin')
# 重置密码
def reset_pw(request):
    if request.method =='GET':
        return render(request, 'forget_pw.html', )
    if request.method == 'POST':
        form = forgetpw(request.POST)
        if form.is_valid():
            flag = False
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
                flag = True
                # 生成随机密码
                strs = string.ascii_letters + string.digits
                pw = random.sample(strs, 8)
                new_password = "".join(pw)
                subject_here = 'GO-学重置密码'
                text_content = '重置后的密码为：' + new_password + ',请保管好新密码，不要给别人。登陆后记得更改密码。'
                send_mail(subject_here, text_content, EMAIL_FROM, [email], fail_silently=False)
                user.set_password(new_password)
                user.save()
                return render(request, 'mi_login.html', {'code': 0, 'error': '注意查收邮箱密码并登陆'})
            except:
                pass
            if not flag:
                return render(request, 'forget_pw.html', {'code':0,'error':'该邮箱未绑定用户'})
        else:
            return render(request, 'forget_pw.html', {'code': 0, 'error': '请输入正确的邮箱'})

# 注销用户
def mi_logout(request):
    logout(request)
    show_class_all = mi_class.objects.all()
    paginator = Paginator(show_class_all, 1, 0)
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
    return render(request, 'index.html', {'page': number, 'paginator': paginator})
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
        email = request.POST.get('email')
        password = request.POST.get('password')
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
# 图片的修改
def imgUpdate(request):
    if request.method=='POST':
        if request.POST.get('sign') == 'lesson_img':
            id = request.POST.get('id')
            if request.FILES.getlist('img'):
                imgfile = request.FILES.getlist('img')[0]
                suffix = os.path.split(str(imgfile))[1]
                suffix_list = ['.png', '.jpg']
                if suffix in suffix_list:
                    class_boject = mi_class.objects.get(id=id)
                    class_boject.class_image = imgfile
                    class_boject.save()
                    return JsonResponse({'code': 1})
                else:
                    return JsonResponse({'code': 0, 'error': '文件格式不对'})
            else:
                return JsonResponse({'code':0,'error':'未上传图片'})
        elif request.POST.get('sign') == 'header_img':
            if request.FILES.getlist('img'):
                imgfile = request.FILES.getlist('img')[0]
                suffix = os.path.split(str(imgfile))[1]
                suffix_list = ['.png', '.jpg']
                if suffix in suffix_list:
                    user_object = request.user
                    user_object.userotherinformtion.headImg = imgfile
                    user_object.userotherinformtion.save()
                    return JsonResponse({'code': 1})
                else:
                    return JsonResponse({'code': 0,'error':'文件格式不对'})
            else:
                return JsonResponse({'code': 0,'error':'未上传图片'})
        else:
            return JsonResponse({'code': 0})
    else:
        return HttpResponse('出现错误了')