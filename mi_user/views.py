from audioop import reverse

from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse,JsonResponse
from . models import *
from mi_class.models import *
from django.core.paginator import Paginator , PageNotAnInteger,EmptyPage

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
            email = request.POST.get('email')
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
                user = User.objects.create_user(telephone=telephone, username=username, password=password1, email=email)
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
                send_email()
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