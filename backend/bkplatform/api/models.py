from django.db import models

# Create your models here.
class User(models.Model):
    account = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = verbose_name = '用户列表'
        db_table = 'users'