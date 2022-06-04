from distutils.command.upload import upload
from email.policy import default
from turtle import right
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