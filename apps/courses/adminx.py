# _*_ coding: utf-8 _*_

import xadmin
from .models import Course, CourseSource, Lesson, Video, BannerCourse


class LessonInline(object):
    model = Lesson
    extre = 0


class CourseSourceInline(object):
    model = CourseSource
    extre = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'learn_times', 'students', 'fav_nums', 'get_lesson_count', 'go_to']
    list_filter = ['name', 'desc', 'detail', 'learn_times', 'students', 'fav_nums']
    search_fields = ['name', 'desc', 'detail', 'learn_times', 'students', 'fav_nums']
    inlines = [LessonInline, CourseSourceInline]
    list_editable = ['desc', 'detail']
    refresh_times = [3, 5]
    style_fields = {'detail': 'ueditor'}


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'learn_times', 'students', 'fav_nums']
    list_filter = ['name', 'desc', 'detail', 'learn_times', 'students', 'fav_nums']
    search_fields = ['name', 'desc', 'detail', 'learn_times', 'students', 'fav_nums']
    inlines = [LessonInline, CourseSourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(fav_nums=0)
        return qs


class CourseSourceAdmin(object):
    list_display = ['course', 'name', 'add_time', 'download']
    list_filter = ['course', 'name', 'add_time', 'download']
    search_fields = ['course', 'name', 'download']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    list_filter = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    list_filter = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(CourseSource, CourseSourceAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)


