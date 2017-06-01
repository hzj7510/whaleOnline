# _*_ coding:utf8 _*_

import json

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password

from .forms import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm, UploadAvatarForm, NewEmailForm, ChangeEmailForm, UserUpdateInfoForm
from .models import UserProfile, EmailVerifyRecord, Banner
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.email_send import email_send_type
from courses.models import Course
from organizations.models import CourseOrg, Teacher
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserFavorite, UserCourse, UserMessage
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            pwd = request.POST.get('password', '')
            user = authenticate(username=username, password=pwd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'error': form.errors})


class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = UserProfile.objects.filter(email=email)
            if user.count() == 0:
                user = UserProfile()
                user.email = email
                user.username = email
                user.is_active = False
                user.password = make_password(password)
                user.save()

                email_send_type(email)

                return render(request, 'login.html')
            else:
                return render(request, 'register.html', {'msg': '用户已存在', 'form': form})
        else:
            return render(request, 'register.html', {'error': form.errors})


class RegisterCodeView(View):
    def get(self, request, code):
        all_records = EmailVerifyRecord.objects.filter(code=code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html')
        else:
            return render(request, 'email-send-message.html', {'msg': '激活失败'})



class ForgetPasswordView(View):
    def get(self, request):
        form = ForgetPasswordForm()
        return render(request, 'forgetpwd.html', {'form': form})

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            user = UserProfile.objects.get(email=email)
            if user:
                email_send_type(email=email, type='forget')
                return render(request, 'email-send-message.html', {'msg': '发送成功'})
            else:
                return render(request, 'forgetpwd.html', {'error': '未查找到该用户'})
        else:
            return render(request, 'forgetpwd.html', {'error': form.errors, 'form': form})


class ResetCodeView(View):
    def get(self, request, code):
        all_record = EmailVerifyRecord.objects.filter(code=code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'email-send-message.html', {'msg', '验证失败'})


class ResetPasswordView(View):
    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')
            if password2 == password1:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(password1)
                user.save()
                return render(request, 'login.html')
            else:
                return render(request, 'password_reset.html', {'msg': '输入密码不同'})
        else:
            return render(request, 'password_reset.html', {'error': form.errors})


class IndexView(View):
    def get(self, request):
        index_courses = Course.objects.all().order_by('-add_time')[:4]
        index_orgs = CourseOrg.objects.all()[:15]
        home_banners = Banner.objects.filter(type='homeBanner')
        model_banners = Banner.objects.filter(type='modelBanner')
        return render(request, 'index.html', {
            'index_courses': index_courses,
            'index_orgs': index_orgs,
            'home_banners': home_banners,
            'model_banners': model_banners,
        })


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {})


class UserUploadAvatarView(View):
    def post(self, request):
        form = UploadAvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponse('{"status":"success", "msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"修改失败"}', content_type='application/json')


class UserUpdatePwdView(View):
    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password2 == password1:
                user = request.user
                user.password = make_password(password1)
                user.save()
                return HttpResponse('{"status":"success", "msg":"修改成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(form.errors), content_type='application/json')


class UserUpdateSendEmailView(LoginRequiredMixin, View):
    def get(self, request):
        form = NewEmailForm(request.GET)
        if form.is_valid():
            email = request.GET.get('email')
            user = UserProfile.objects.filter(email=email)
            if user:
                return HttpResponse('{"status": "failure", "msg": "邮箱已存在"}', content_type='application/json')
            else:
                email_send_type(email, 'change')
                return HttpResponse('{"status": "success", "msg": "发送成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(form.errors), content_type='application/json')


class UserUpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            code = request.POST.get('code')
            email_verify = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='change')
            if email_verify:
                user = request.user
                user.email = email
                user.save()
                return HttpResponse('{"status": "success", "msg": "修改成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "修改失败"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "修改失败"}', content_type='application/json')


class UserUpdateInfoView(LoginRequiredMixin, View):
    def post(self, request):
        form = UserUpdateInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponse('{"status": "success", "msg": "保存成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(form.errors), content_type='application/json')


class UserMyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        courses = [user_course.course for user_course in user_courses]
        return render(request, 'usercenter-mycourse.html', {
            'courses': courses

        })


class UserFavView(LoginRequiredMixin, View):
    def get(self, request, fav_type):
        favs = UserFavorite.objects.filter(user=request.user, fav_type=int(fav_type))
        if int(fav_type) == 1:
            course_ids = [fav.fav_id for fav in favs]
            courses = Course.objects.filter(id__in=course_ids)
            return render(request, 'usercenter-fav-course.html', {
                'courses': courses,
            })
        elif int(fav_type) == 2:
            org_ids = [fav.fav_id for fav in favs]
            orgs = CourseOrg.objects.filter(id__in=org_ids)
            return render(request, 'usercenter-fav-org.html', {
                'orgs': orgs,
            })
        else:
            teacher_ids = [fav.fav_id for fav in favs]
            teachers = Teacher.objects.filter(id__in=teacher_ids)
            return render(request, 'usercenter-fav-teacher.html', {
                'teachers': teachers,
            })


class UserMessagesView(LoginRequiredMixin, View):
    def get(self, request):
        user_messages = UserMessage.objects.filter(user=request.user.id)
        for user_message in user_messages:
            user_message.has_read = True
            user_message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(user_messages, 1, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'user_messages': messages,
        })


class MyResumeView(View):
    def get(self, request):
        return render(request, 'resume.html', {})

class MyResumePythonView(View):
    def get(self, request):
        return render(request, 'resume-python.html', {})

def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
