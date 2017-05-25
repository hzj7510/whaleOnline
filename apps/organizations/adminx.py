# _*_ coding: utf-8 _*_

import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    list_filter = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    ordering = ['-add_time']
    readonly_fields = ['desc']
    exclude = ['add_time']
    relfield_style = 'fk-ajax'


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'image', 'address', 'city', 'click_num', 'fav_num']
    list_filter = ['name', 'desc', 'image', 'address', 'city', 'click_num', 'fav_num']
    search_fields = ['name', 'desc', 'image', 'address', 'city', 'click_num', 'fav_num']


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_year', 'work_position', 'work_company', 'point', 'age', 'click_num', 'fav_num']
    list_filter = ['name', 'org', 'work_year', 'work_position', 'work_company', 'point', 'age', 'click_num', 'fav_num']
    search_fields = ['name', 'org', 'work_year', 'work_position', 'work_company', 'point', 'age', 'click_num', 'fav_num']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
