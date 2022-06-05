from django.db import models

# Create your models here.
class User(models.Model):
    account = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = verbose_name = '用户列表'
        db_table = 'users'

class ValidateImages(models.Model):
    imgurls = models.TextField()
    right = models.CharField(max_length=9,default='-2')

    class Meta:
        verbose_name_plural = verbose_name = '验证图片'
        db_table = 'validate_imgs'

class History(models.Model):
    his_uuid = models.CharField(max_length=128)
    username = models.CharField(max_length=64)
    length = models.IntegerField()
    pro_length = models.IntegerField(default=0)
    imgurls = models.TextField()
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = '历史记录'
        db_table = 'historyrecord'  

class Feedback(models.Model):
    check = models.CharField(max_length=32)
    text = models.TextField()

    class Meta:
        verbose_name_plural = verbose_name = '反馈表'
        db_table = 'feedback'
