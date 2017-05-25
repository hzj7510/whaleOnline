# _*_ coding:utf8 _*_

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'用户昵称')
    gender = models.CharField(max_length=10, verbose_name=u'用户性别', choices=(('female', '女'), ('male', '男')), default='female')
    address = models.CharField(max_length=50, verbose_name=u'用户地址')
    birday = models.DateField(verbose_name=u'用户生日', blank=True, null=True)
    mobile = models.CharField(verbose_name=u'手机号码', max_length=11, null=True, blank=True)
    image = models.ImageField(verbose_name=u'头像', upload_to='image/%Y/%m', default='image/default.png/')

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def get_message_count(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'邮箱注册')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(choices=(('register', '注册'), ('forget', '忘记密码'), ('change','修改邮箱')), default='register', max_length=10)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.email


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name=u'轮播图片')
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    index = models.IntegerField(default=0, verbose_name=u'排序位置')
    type = models.CharField(default='homeBanner', choices=(('homeBanner', '首页banner图'), ('modelBanner', '首页modelBanner图')), max_length=15, verbose_name=u'banner图类型')

    class Meta:
        verbose_name = u'轮播'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
