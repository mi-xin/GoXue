from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField


import os
# 重写 UserMangager
class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password,**kwargs):
        if not telephone:
            raise ValueError("请填入手机号码！")
        if not username:
            raise ValueError("请输入用户名！")
        if not password:
            raise ValueError("请填入密码!")
        user = self.model(telephone=telephone,username=username,password=password,**kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_user(self, telephone, username, password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)
    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone, username, password, **kwargs)
# 重写User
class User(AbstractBaseUser,PermissionsMixin):
    uid = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=18, verbose_name='用户名')
    telephone = models.CharField(max_length=11, unique=True, verbose_name='手机号码')
    email = models.EmailField(unique=True, verbose_name='邮箱',null=True)
    is_active = models.BooleanField(default=True, verbose_name='是否为激活用户')
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
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
