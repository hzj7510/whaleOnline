# _*_ coding:utf8 _*_

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, Lesson, CourseSource
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, UserCourse, CourseComment
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self, request):
        course_list = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        sort = request.GET.get('sort', '')
        keywords = request.GET.get('keywords', '')
        if keywords:
            course_list = course_list.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(detail__icontains=keywords))

        if sort == 'hot':
            course_list = course_list.order_by('-click_nums')
        elif sort == 'students':
            course_list = course_list.order_by('-students')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(course_list, 3, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'course_list': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        lesson_count = course.lesson_set.all().count()
        # user_courses = UserCourse.objects.filter(course=course)[:3]
        org_is_fav = False
        course_is_fav = False
        if request.user.is_authenticated():
            org_fav = UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course.course_org.id)
            if org_fav:
                org_is_fav = True
            course_fav = UserFavorite.objects.filter(user=request.user, fav_type=1, fav_id=course.id)
            if course_fav:
                course_is_fav = True
        tag = course.tag
        recommend_courses = []
        if tag:
            recommend_courses = Course.objects.filter(~Q(id=course.id), tag=tag)[:2]

        course.click_nums += 1
        course.save()

        return render(request, 'course-detail.html', {
            'course': course,
            'lesson_count': lesson_count,
            'org_is_fav': org_is_fav,
            'course_is_fav': course_is_fav,
            'recommend_courses': recommend_courses
        })

    def post(self, request, course_id):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        fav_type = request.POST.get('fav_type', 0)
        fav_id = request.POST.get('fav_id', 0)

        if int(fav_type) < 0 and int(fav_id) < 0:
            return HttpResponse('{"status":"fail","msg":"收藏失败"}', content_type='application/json')
        fav = UserFavorite.objects.filter(user=request.user, fav_type=int(fav_type), fav_id=int(fav_id))
        if fav:
            fav.delete()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            fav = UserFavorite()
            fav.user = request.user
            fav.fav_id = fav_id
            fav.fav_type = fav_type
            fav.save()
            return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')


class DetailLessonView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        lesson_list = Lesson.objects.filter(course=course)
        sources = CourseSource.objects.filter(course=course)[:1]
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course_n = UserCourse()
            user_course_n.user = request.user
            user_course_n.course = course
            user_course_n.save()

        learn_courses = UserCourse.objects.filter(~Q(course=course), user=request.user)[:2]
        return render(request, 'course-video.html', {
            'course': course,
            'lesson_list': lesson_list,
            'sources': sources,
            'learn_courses': learn_courses,
        })


class DetailCommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        all_comments = CourseComment.objects.filter(course=course)

        return render(request, 'course-comment.html', {
            'course': course,
            'all_comments': all_comments
        })


class DetailAddCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments')
        course = Course.objects.get(id=int(course_id))
        if int(course_id) == 0:
            return HttpResponse('{"status": "fail", "msg": "添加错误"}', content_type='application/json')
        course_comment = CourseComment()
        course_comment.comment = comments
        course_comment.user = request.user
        course_comment.course = course
        course_comment.save()
        return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')

