# _*_ coding:utf8 _*_

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.forms import UserAskForm
from operation.models import UserFavorite
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class OrgCourseListView(View):
    def get(self, request):
        org_list = CourseOrg.objects.all()
        org_count = org_list.count()
        city_list = CityDict.objects.all()
        hot_orgs = CourseOrg.objects.order_by('-click_num')[:3]
        keywords = request.GET.get('keywords', '')
        if keywords:
            org_list = org_list.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        city_id = request.GET.get('city', '')
        if city_id:
            org_list = org_list.filter(city_id=int(city_id))

        ct = request.GET.get('ct', '')
        if ct:
            org_list = org_list.filter(category=ct)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                org_list = org_list.order_by('-students')
            elif sort == 'courses':
                org_list = org_list.order_by('-course_num')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(org_list, 3, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'org_list': orgs,
            'city_list': city_list,
            'org_count': org_count,
            'city_id': city_id,
            'ct': ct,
            'hot_orgs': hot_orgs,
            'sort': sort,
        })


class UserAskView(View):
    def post(self, request):
        form = UserAskForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加出错"}', content_type='application/json')


class DetailHomePageView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        all_course = org.course_set.all()[:3]
        all_teacher = org.teacher_set.all()[:3]
        org_type = 'homepage'
        is_fav = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2)
            if user_fav:
                is_fav = True

        return render(request, 'org-detail-homepage.html', {
            'org': org,
            'all_course': all_course,
            'all_teacher': all_teacher,
            'org_type': org_type,
            'is_fav': is_fav,
        })

    def post(self, request):
        pass


class DetailCourseView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        all_course = org.course_set.all()
        org_type = 'course'
        is_fav = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2)
            if user_fav:
                is_fav = True

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, 1, request=request)

        courses = p.page(page)

        return render(request, 'org-detail-course.html', {
            'org': org,
            'all_course': courses,
            'org_type': org_type,
            'is_fav': is_fav,
        })

    def post(self, request):
        pass


class DetailTeacherView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = org.teacher_set.all()
        org_type = 'teacher'
        is_fav = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2)
            if user_fav:
                is_fav = True
        # try:
        #     page = request.GET.get('page', 1)
        # except PageNotAnInteger:
        #     page = 1
        #
        # p = Paginator(all_teacher, 1, request=request)
        #
        # teacher = p.page(page)

        return render(request, 'org-detail-teachers.html', {
            'org': org,
            'all_teacher': all_teacher,
            'org_type': org_type,
            'is_fav': is_fav,
        })

    def post(self, request):
        pass


class DetailDescView(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        org_type = 'desc'
        is_fav = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2)
            if user_fav:
                is_fav = True

        # try:
        #     page = request.GET.get('page', 1)
        # except PageNotAnInteger:
        #     page = 1
        #
        # p = Paginator(all_teacher, 1, request=request)
        #
        # teacher = p.page(page)

        return render(request, 'org-detail-desc.html', {
            'org': org,
            'org_type': org_type,
            'is_fav': is_fav,
        })

    def post(self, request):
        pass


class DetailCollectionView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg": "用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_type=int(fav_type), fav_id=int(fav_id))
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg": "收藏"}', content_type='application/json')
        else:
            if fav_id > 0 and fav_type > 0:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                return HttpResponse('{"status":"success", "msg": "已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg": "收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        teacher_list = Teacher.objects.all()
        teacher_count = Teacher.objects.all().count()
        order_teachers = Teacher.objects.all().order_by('-work_year')[:3]
        sort = request.GET.get('sort', '')
        keywords = request.GET.get('keywords', '')
        if keywords:
            teacher_list = teacher_list.filter(name__icontains=keywords)

        if sort:
            teacher_list = teacher_list.order_by('-fav_num')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(teacher_list, 2, request=request)

        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'teacher_list': teachers,
            'teacher_count': teacher_count,
            'order_teachers': order_teachers,
            'sort': sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        order_teachers = Teacher.objects.all().order_by('-work_year')[:3]
        org_has_fav = False
        teacher_has_fav = False
        if request.user.is_authenticated():
            teacher_fav = UserFavorite.objects.filter(fav_id=teacher.id, fav_type=3, user=request.user)
            if teacher_fav:
                teacher_has_fav = True
            org_fav = UserFavorite.objects.filter(fav_id=teacher.org.id, fav_type=2, user=request.user)
            if org_fav:
                org_has_fav = True
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'org_has_fav': org_has_fav,
            'teacher_has_fav': teacher_has_fav,
            'order_teachers': order_teachers,

        })


class TeacherFavView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg":"用户未登录"}', content_type='application/json')
        fav_id = request.POST.get('fav_id')
        fav_type = request.POST.get('fav_type')
        user_fav = UserFavorite.objects.filter(user=request.user, fav_type=fav_type, fav_id=fav_id)
        if user_fav:
            user_fav.delete()
            return HttpResponse('{"status": "success", "msg":"收藏"}', content_type='application/json')
        else:
            fav = UserFavorite(user=request.user, fav_type=fav_type, fav_id=fav_id)
            fav.save()
            return HttpResponse('{"status": "success", "msg":"已收藏"}', content_type='application/json')
