# _*_ coding: utf-8 _*_

import re

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class NewEmailForm(forms.Form):
    email = forms.EmailField(required=True)


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(required=True)
    code = forms.CharField(required=True, max_length=4, min_length=4)


class UserUpdateInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码非法', code='mobile_invalid')
