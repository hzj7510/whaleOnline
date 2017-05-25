# _*_ coding:utf8 _*_

from __future__ import unicode_literals

from django.db import models
from datetime import datetime


# from courses.models import Course
# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=120, verbose_name=u'城市名称')
    desc = models.CharField(max_length=120, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'机构名')
    image = models.ImageField(upload_to='organization/%Y/%m', verbose_name=u'课程图片')
    desc = models.CharField(max_length=100, verbose_name=u'课程描述')
    address = models.CharField(max_length=100, verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, verbose_name=u'城市')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_num = models.IntegerField(default=0, verbose_name=u'课程数')
    category = models.CharField(choices=(('pxjg', u'培训机构'), ('gx', u'高效'), ('gr', u'个人')), max_length=6, default='gx', verbose_name=u'类别')
    fav_num = models.IntegerField(default=0, verbose_name=u'收藏人数')

    class Meta:
        verbose_name = u'机构'
        verbose_name_plural = verbose_name

    def get_course_count(self):
        return self.course_set.all().count()

    def get_courses(self):
        return self.course_set.all()[:3]

    def get_teacher_count(self):
        return self.teacher_set.all().count()

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'所在机构')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name=u'头像', null=True, blank=True)
    name = models.CharField(verbose_name=u'教师名', max_length=10)
    work_year = models.IntegerField(verbose_name=u'工作年限', default=0)
    work_position = models.CharField(max_length=50, verbose_name=u'公司职位')
    work_company = models.CharField(max_length=50, verbose_name=u'所在公司')
    point = models.CharField(max_length=100, verbose_name=u'教学特点')
    age = models.IntegerField(verbose_name=u'年龄', default=18)
    fav_num = models.IntegerField(default=0, verbose_name=u'关注人数')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    need_know = models.CharField(default='', verbose_name=u'课程须知', max_length=200)
    learn_what = models.CharField(default='', verbose_name=u'能学到什么', max_length=200)

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def get_all_course(self):
        return self.course_set.all()

    def __unicode__(self):
        return self.name


