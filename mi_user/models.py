from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django import forms
from mi_class.models import *
import os
# 重写 UserMangager
class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError("请填入手机号码！")
        if not username:
            raise ValueError("请输入用户名！")
        if not password:
            raise ValueError("请填入密码!")
        # if not is_teacher:
        #     raise ValueError("请选择您的身份!")
        user = self.model(telephone=telephone,username=username,password=password,**kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_user(self, telephone, username, password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)
    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(telephone, username, password, **kwargs)
# 重写User
class User(AbstractBaseUser,PermissionsMixin):
    uid = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=18, verbose_name='用户名')
    # password = models.CharField(verbose_name='密码,', max_length=30)
    telephone = models.CharField(max_length=11, unique=True, verbose_name='手机号码')
    email = models.EmailField(unique=True, verbose_name='邮箱',null=True)
    is_active = models.BooleanField(default=True, verbose_name='是否为激活用户')
    # is_student = models.BooleanField(default=False, verbose_name='是否为学生')
    # is_teacher = models.BooleanField(default=False, verbose_name='是否为教师')
    is_staff = models.BooleanField(default=False, verbose_name='是否为员工')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 以telephone 作为验证
    USERNAME_FIELD = 'telephone'
    # 创建超级用户需要的字段
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username
    def get_short_name(self):
        return self.username

# 用户的其他信息
class UserOtherInformtion(models.Model):
    headImg = models.ImageField(verbose_name='头像', upload_to='img/', default="img/default.jpg")
    user = models.OneToOneField(User,on_delete=models.CASCADE)
# 登陆注册校验表单
class miregister(forms.Form):
    username = forms.CharField(max_length=18, required=True)
    password1 = forms.CharField(max_length=30, required=True)
    password2 = forms.CharField(max_length=30, required=True)
    telephone = forms.CharField(max_length=11, required=True)
class milogin(forms.Form):
    password = forms.CharField(max_length=30, required=True)
    telephone = forms.CharField(max_length=11, required=True)

# 修改密码校验
class udpassword(forms.Form):
    old_password = forms.CharField(max_length=30, required=True)
    new_password = forms.CharField(max_length=30, required=True)
