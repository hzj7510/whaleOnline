# _*_ coding: utf-8 _*_


from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from NewMXOnline.settings import EMAIL_FROM


def generate_random_str(random_length=4):
    random_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkIiMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        random_str += chars[random.randint(0, length)]
    return random_str


def email_send_type(email, type='register'):
    email_record = EmailVerifyRecord()
    random_str = generate_random_str()
    email_record.code = random_str
    email_record.email = email
    email_record.send_type = type
    email_record.save()

    if type == 'register':
        email_title = '鲸之网在线注册激活链接'
        email_body = '请点击下面的连接激活你的账号: http://127.0.0.1:8000/active/{0}'.format(random_str)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    if type == 'forget':
        email_title = '鲸之网密码重置连接'
        email_body = '请点击下面的连接重置你的账号: http://127.0.0.1:8000/reset/{0}'.format(random_str)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    if type == 'change':
        email_title = '鲸之网邮箱重置连接'
        email_body = '您的验证码是: {0}'.format(random_str)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

