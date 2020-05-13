from django.db import models

# Create your models here.


class User(models.Model):
    '''用户表'''
    gender = (
        ('male','男'),
        ('female','女'),
    )
    poster = (
        ('manager', '管理员'),
        ('worker', '操作员'),
    )
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=False)
    phone = models.CharField(max_length=50,default='')
    sex = models.CharField(max_length=32,choices=gender,default='male')
    role = models.CharField(max_length=32, choices=poster, default='manager')
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'
