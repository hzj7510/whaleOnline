# _*_ coding: utf-8 _*_
from django.conf.urls import url

from .views import LoginView, LogoutView, RegisterView, ForgetPasswordView, ResetPasswordView, UserInfoView, UserUploadAvatarView, UserUpdatePwdView, UserUpdateSendEmailView, UserUpdateEmailView, UserUpdateInfoView
from .views import UserMyCourseView, UserFavView, UserMessagesView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^forget/$', ForgetPasswordView.as_view(), name='forgetPwd'),
    url(r'^reset/pwd$', ResetPasswordView.as_view(), name='reset'),
    url(r'^center/info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^upload/avatar/$', UserUploadAvatarView.as_view(), name='upload_avatar'),
    url(r'^update/pwd/$', UserUpdatePwdView.as_view(), name='update_pwd'),
    url(r'^sendemail_code/$', UserUpdateSendEmailView.as_view(), name='update_send_code'),
    url(r'^update_email/$', UserUpdateEmailView.as_view(), name='update_email'),
    url(r'^info/$', UserUpdateInfoView.as_view(), name='update_email'),
    url(r'^mycourses/$', UserMyCourseView.as_view(), name='my_courses'),
    url(r'^fav/(?P<fav_type>\d+)/$', UserFavView.as_view(), name='fav'),
    url(r'^message/$', UserMessagesView.as_view(), name='message'),

]
