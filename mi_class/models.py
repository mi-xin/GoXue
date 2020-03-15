from django.db import models
from mi_user.models import User
# Create your models here.

# 课程模型
class mi_class(models.Model):
    class_image = models.ImageField(verbose_name='封面图',upload_to='img/', blank=True,default="img/default.jpg")
    title = models.CharField(max_length=100)
    file = models.ManyToManyField('mi_voide')
    introduce = models.TextField()
    author = models.CharField(max_length=15, default='aa')
    create_user = models.ForeignKey(User,related_name = 'create_user', on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='是否删除',default=True)
    is_release = models.BooleanField(verbose_name='是否已发布',default=False)
    create_data = models.DateTimeField(auto_now_add=True)
# 课程章节模型
class class_chapter(models.Model):
    name = models.CharField(verbose_name='章节名',max_length=100)
    class_model = models.ForeignKey(mi_class,verbose_name='课程', on_delete=models.CASCADE, related_name='class_name')
# 视频模型
class mi_voide(models.Model):
    file = models.FileField(upload_to="video")
    file_name = models.CharField(max_length=100)
    chapter_name = models.ForeignKey(class_chapter, related_name='class_chapter', on_delete=models.CASCADE)
# 评论模型
class Comment(models.Model):
    lesson = models.ForeignKey(mi_class,verbose_name='评论的课程', on_delete=models.CASCADE,related_name='lessonComment',null=False)
    user = models.ForeignKey(User, verbose_name='评论用户',on_delete=models.CASCADE, related_name='comment_user',null=False)
    content = models.TextField(verbose_name='评论内容',null=True,blank=True)
    data = models.DateField(verbose_name='评论时间',auto_now_add=True)
class Reply(models.Model):
    user = models.ForeignKey(User, verbose_name='回复用户', on_delete=models.CASCADE, related_name='reply_user',
                                null=False)
    content = models.TextField(verbose_name='回复内容', null=True, blank=True)
    data = models.DateField(verbose_name='评论时间', auto_now_add=True)
    commentUpper = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, verbose_name='上一级评论对象',
                                     related_name='commentUpper')