from django.db import models
from mi_user.models import *
# Create your models here.
class mi_voide(models.Model):
    file = models.FileField(upload_to="video")
    file_name = models.CharField(max_length=100)
    class_name = models.ForeignKey('mi_class', related_name='class_name', on_delete='CASCADE')
class mi_class(models.Model):
    class_image = models.ImageField(verbose_name='封面图',upload_to='img/',blank=True)
    title = models.CharField(max_length=100)
    file = models.ManyToManyField('mi_voide')
    introduce = models.TextField()
    author = models.CharField(max_length=15, default='aa')
    create_user = models.ForeignKey('mi_user.User',related_name = 'create_user', on_delete='CASCADE')
    is_release = models.BooleanField(verbose_name='是否已发布',default=False)