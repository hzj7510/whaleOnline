# _*_ coding: utf-8 _*_

from django.conf.urls import url

from .views import OrgCourseListView, UserAskView, DetailHomePageView, DetailCourseView, DetailTeacherView, DetailDescView, DetailCollectionView, TeacherListView, TeacherDetailView, TeacherFavView

urlpatterns = [
    url(r'^list/', OrgCourseListView.as_view(), name='list'),
    url(r'^add_ask/', UserAskView.as_view(), name='add_ask'),
    url(r'^detail/homepage/(?P<org_id>\d+)/$', DetailHomePageView.as_view(), name='detail_homepage'),
    url(r'^detail/course/(?P<org_id>\d+)/$', DetailCourseView.as_view(), name='detail_course'),
    url(r'^detail/teacher/(?P<org_id>\d+)/$', DetailTeacherView.as_view(), name='detail_teacher'),
    url(r'^detail/desc/(?P<org_id>\d+)/$', DetailDescView.as_view(), name='detail_desc'),
    url(r'^detail/collection/$', DetailCollectionView.as_view(), name='detail_collection'),
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
    url(r'^teacher/fav/$', TeacherFavView.as_view(), name='teacher_fav'),


]