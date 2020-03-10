from django.db import models
from mi_user.models import *
# Create your models here.
# 视频模型
class mi_voide(models.Model):
    file = models.FileField(upload_to="video")
    file_name = models.CharField(max_length=100)
    chapter_name = models.ForeignKey('class_chapter', related_name='class_chapter', on_delete='CASCADE')
# 课程模型
class mi_class(models.Model):
    class_image = models.ImageField(verbose_name='封面图',upload_to='img/', blank=True,default="img/default.jpg")
    title = models.CharField(max_length=100)
    file = models.ManyToManyField('mi_voide')
    introduce = models.TextField()
    author = models.CharField(max_length=15, default='aa')
    create_user = models.ForeignKey('mi_user.User',related_name = 'create_user', on_delete='CASCADE')
    is_release = models.BooleanField(verbose_name='是否已发布',default=False)
    create_data = models.DateTimeField(auto_now_add=True)
# 课程章节模型
class class_chapter(models.Model):
    name = models.CharField(verbose_name='章节名',max_length=100)
    class_model = models.ForeignKey('mi_class',verbose_name='课程',on_delete='CASCADE',related_name='class_name')
# 课程创建校验
class Upload_class(forms.Form):
    title = forms.CharField(label="课程名", error_messages={"required": "课程名必填"},)
    introduce = forms.CharField(label="简介", error_messages={"required": "简介必填"})