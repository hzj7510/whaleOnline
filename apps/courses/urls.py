# _*_ coding: utf-8 _*_

from django.conf.urls import url

from .views import CourseListView, CourseDetailView, DetailLessonView, DetailCommentsView, DetailAddCommentsView

urlpatterns = [
    url(r'^list/', CourseListView.as_view(), name='list'),

    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='detail'),

    url(r'^detail/lesson/(?P<course_id>\d+)', DetailLessonView.as_view(), name='lesson'),

    url(r'^detail/comments/(?P<course_id>\d+)', DetailCommentsView.as_view(), name='comments'),

    url(r'^detail/add_comment/$', DetailAddCommentsView.as_view(), name='add_comments'),
]
