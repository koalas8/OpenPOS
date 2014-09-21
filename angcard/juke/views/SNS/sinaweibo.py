#encoding=utf-8

import urllib2
import uuid
import os
import hashlib
import random
from flask import redirect
from flask.json import jsonify
from flask import render_template
from flask import request
from flask import session
from flask.views import MethodView
from juke import app
from juke.modules import *
from juke.views.users import add_new as add_new_user
from juke.views.users import Login
from juke.utils.myemail import MyEmail
from weibo import APIClient


# SINA 微博返回的错误信息格式
# {
#     "error_code" : "403",
#     "request" : "/statuses/friends_timeline.json",
#     "error" : "40302:Error: auth faild!"
# }
#
# 聚客100官方微博账号密码：
# service@juke100.com
# 0101001101010011

APP_KEY = app.config['SINA_WEIBO_APP_KEY']
APP_SECRET = app.config['SINA_WEIBO_APP_SECRET']
CALLBACK_URL = app.config['DOMAIN'] + '/weibo/sina/login/callback'


def is_error_resp(resp):
    ''' 判断新浪微博是否返回了错误信息
        @resp 新浪微博的返回信息, json格式
    '''
    if 'error_code' in resp.keys():
        return True
    else:
        return False


def get_client():
    ''' 生成新浪微博SDK的client
    '''
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    return client


def fetch_profile_image(url, profile_image):
    '''
    下载用户头像到本地,并删除旧的头像文件（如果有的话）
    @param url: 要下载的用户头像http地址
    @param profile_image: 原有的头像名,不包括路径
    @return 新的头像文件名,不包括路径
    '''
    profile_image = None if profile_image is None or profile_image.strip() == '' else profile_image
    if profile_image:
        try:
            old_profile = '%s/%s' % (app.config['PROFILE_IMG_DIR'], profile_image)
            if os.path.isfile(old_profile):
                os.remove(old_profile)
            else:
                pass
        except IOError, e:
            pass
    req = urllib2.urlopen(url)
    profile_image = str(uuid.uuid4())  # 获取到image后的本地命名
    f = open('%s/%s' % (app.config['PROFILE_IMG_DIR'], profile_image), 'wb')
    f.write(req.read())
    f.close()
    return profile_image

#
# class SinaWeiboRegisterProcess(MethodView):
#     def post(self):
#         i = request.args
#         action = i.get('action', '').strip()
#         email = request.json.get('email', '').strip()
#
#
#
#         if action == '1':  # 发送验证码
#             # 生成验证码
#             passcode = str(random.randrange(100000, 999999))
#             em = MyEmail()
#             em_result = em.send_email(_from=app.config['EMAIL_ACCOUNT'],
#                                       password=app.config['EMAIL_PASSWORD'],
#                                       to=email, subject=u'聚客100验证码',
#                                       content=u'以下是您在聚客100注册时使用的验证码: %s' % passcode)
#             if em_result:
#                 return jsonify(success=True)
#             return jsonify(success=False, msg=u'发送邮件失败')
#
#         if action == '2':  # 提交验证
#             pass

# class SinaWeiboRegister(MethodView):
#     def get(self):
#         return render_template('/sns/sina/weibo_register.html')
#
#     def post(self):
#         # 先尝试用sina weibo 的 uid 作为 user_no 注册，如果user_no已存在，再跳转到输入email页面，以email作为user_no登录
#         user_no = uid = session['sina_weibo_uid']
#
#         # 如果user_no存在
#         if db_session.query(UserInfo).filter(UserInfo.user_no == user_no).count():
#             return render_template('/sns/sina/weibo_register_input_email.html')
#
#         # user_no不存在，直接使用user_no注册
#         password = uid[:6]
#         shop_name = u'我的商铺'
#         from_weibo = True
#         api = '1'
#
#         result = add_new_user(user_no, password, shop_name, from_weibo=True, api=api)
#         if result:  # result != {}
#             # 说明使用微博注册成功, 更新用户信息
#             user = db_session.query(UserInfo).filter(UserInfo.user_no == uid).one()
#             user.sina_weibo_uid = uid
#             user.sina_weibo_token = session['sina_weibo_token']
#             db_session.add(user)
#             db_session.commit()
#             return redirect('/weibo/sina/login')  # 使用微博登录
#         else:  # 注册失败
#             title = u'注册时出错'
#             msg = u'不能根据您的微博账号自动注册聚客系统'
#             links = [{'href': '/user/register', 'label': u'返回到注册页面'}]
#             return render_template('info.html', **locals())


class SinaWeiboBinding(MethodView):
    def get(self):
        return render_template('/sns/sina/register.html')

    def post(self):
        # 获取用户输入的要绑定的聚客账号信息
        # 绑定前要核对用户名、密码是否正确。核对通过后才能绑定
        i = request.form
        unit_no = i.get('unit_no', '').strip()
        user_no = i.get('user_no', '').strip()
        password = i.get('password', '').strip()

        q = db_session.query(UserInfo).filter(UserInfo.user_no == user_no).filter(UserInfo.unit_no == unit_no)
        if not q.count():
            return jsonify(success=False, msg=u'无此用户')

        user = q.one()
        if user.status != '0':
            return jsonify(success=False, msg=u'此用户已停用')

        if user.password != hashlib.md5(password).hexdigest():
            return jsonify(success=False, msg=u'密码不正确')

        # 检查通过，绑定
        user.sina_weibo_account = session['sina_weibo_uid']
        user.sina_token = session['sina_weibo_token']
        db_session.add(user)
        db_session.commit()

        # 绑定成功，使用微博登录系统
        return redirect('/weibo/sina/login')


class SinaWeiboLogin(MethodView):
    ''' 新浪微博登陆
    '''
    def get(self):
        client = get_client()
        url = client.get_authorize_url()
        return redirect(url)


class SinaWeiboLoginCallback(MethodView):
    ''' 新浪微博登陆callback
        在此处理登陆成功与否
    '''
    def get(self):
        code = request.args.get('code', '').strip()
        client = get_client()
        r = client.request_access_token(code)
        access_token = r.access_token
        expires_in = r.expires_in
        client.set_access_token(access_token, expires_in)

        resp = client.account.get_uid.get()
        if is_error_resp(resp):
            title = u'登录出错'
            msg = u'不能获取您在新浪微博上的账号名，请重试'
            links = [{'href': '/user/login', 'label': u'返回到登录页面'}]
            return render_template('info.html', **locals())

        uid = str(resp.uid)  # 获取主账号
        password = str(uid)  # 取微博账号的前6位作为聚客系统的密码        

        # 检查微博账号是否已在聚客中绑定？
        # 如果未绑定，则跳转到绑定页面，需要提供一个邮箱，并且验证通过后才能绑定
        q = db_session.query(UserInfo).filter(UserInfo.sina_weibo_uid == uid)
        if not q.count():  # 未绑定
            # 设置session, 绑定微博账号时用
            session['sina_weibo_uid'] = uid
            session['sina_weibo_token'] = access_token

            return redirect('/weibo/sina/bind')

        # 已绑定
        login = Login()
        login.username = uid
        login.password = password
        login.come_from_code = '1'
        resp = login.post()
        return resp
