# _*_ coding:utf8 _*_

from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from DjangoUeditor.models import UEditorField
from organizations.models import CourseOrg, Teacher
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = UEditorField(verbose_name=u'课程详情',width=600, height=300, imagePath="courses/ueditor/", filePath="courses/ueditor/", default='')
    degree = models.CharField(max_length=5, choices=(('cj', u'初级'), ('zj', u'中级'), ('gj',u'高级')), default='cj')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'关注人数')
    image = models.ImageField(verbose_name=u'课程头像', upload_to='courses/%Y/%m')
    click_nums = models.IntegerField(verbose_name=u'点击数', default=0)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)
    teacher = models.ForeignKey(Teacher, verbose_name=u'授课教师', null=True, blank=True)
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    tag = models.CharField(max_length=10, verbose_name=u'标签', default='')
    kind = models.CharField(choices=(('qd', '前段'), ('hd', '后端'), ('ydd', '移动端')), default='ydd', verbose_name=u'类别', max_length=5)

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_learn_user(self):
        return self.usercourse_set.all()[:3]

    def get_all_source(self):
        return self.coursesource_set.all()[:3]

    def get_lesson_count(self):
        return self.lesson_set.all().count()
    get_lesson_count.short_description = '章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com'>跳转</>")
    go_to.short_description = '跳转'

    def __unicode__(self):
        return self.name


#这里继承Course
class BannerCourse(Course):
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        #这里是关键 proxy为True后就不会创建新表了
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def get_all_video(self):
        return self.video_set.all()

    def __unicode__(self):
        return self.name


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节名')
    url = models.URLField(max_length=100, verbose_name=u'视频地址', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseSource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'资源名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
