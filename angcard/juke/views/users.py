#-*- coding=utf-8 -*-
import uuid
import hashlib
import qrcode
import sys
from flask import session, redirect
from flask import request
from flask import render_template
from flask import make_response
from flask import Blueprint
from flask.json import jsonify
from flask.views import MethodView
from sqlalchemy import and_
from sqlalchemy import update
from juke.utils.myemail import MyEmail
from juke.modules import *
from juke import rspmsg
from juke import app
from juke import authority
from juke.utils.captcha import  create_captcha


def add_new(user_no, password, shop_name, from_weibo=False, api='0', real_name='', profile_image='', email=''):
    ''' 添加新用户，并自动生成新用户的集团号、商户号、终端号
        适合自主注册用户
        添加成功返回 '0'
        @return {'user_no': user_no, 'shop_name': shop_name, 'real_name': real_name, 'token': token}
    '''
    # 注册时要根据算法确定集团号，产生token, 并将状态确定为预注册状态(标识号:2, 如果是微博注册,则标识号是0)
    # 向用户发送一封注册确认邮件
    # 算法：UUID选前8位作为集团号，如果选择的集团号已存在，则重新选择
    token = str(uuid.uuid4())
    unit_no = token[:8]
    # TODO: 判断邮箱格式是否合法
    while db_session.query(UnitInfo).filter(UnitInfo.unit_no == unit_no).count():  # 此循环是为了防止注册时集团号重复
        token = str(uuid.uuid4)
        unit_no = token[:8]
    shop_no = token.replace('-', '')[:15]
    terminal_no = token.replace('-', '')[:8]
    md5_password = hashlib.md5(password).hexdigest()
    is_admin = False
    role_no = str(uuid.uuid4())
    user_level = 'unit'
    status = '0' if from_weibo else '2'

    # 生成数据库记录,集团名称与商户名称相同。
    unit = UnitInfo(unit_no=unit_no, unit_name=shop_name, status='2', remark=u'免费用户')
    shop = ShopInfo(shop_no=shop_no, shop_name=shop_name, status='2', remark=u'免费用户', unit_no=unit_no)
    terminal = TerminalInfo(terminal_no=terminal_no, status='2', shop_no=shop_no, is_default=True,
                            des_key=str(uuid.uuid4()))
    role = RoleInfo(unit_no=unit_no, role_no=role_no, role_name=u'免费用户权限', creator='sys')
    user = UserInfo(user_no=user_no, password=md5_password, unit_no=unit_no, shop_no=shop_no,
                    is_admin=is_admin, role_no=role_no, user_level=user_level, token=token,
                    status=status, email=email, api=api)  # status=2 预注册，验证token后转为正常状态
    try:
        db_session.add(unit)
        db_session.flush()
        db_session.add(shop)
        db_session.flush()
        db_session.add(terminal)
        db_session.flush()
        db_session.add(role)
        db_session.flush()
        db_session.add(user)
        db_session.flush()
        # 设置默认权限
        for operation_code in ['00800', '00801', '00802', '00803', '00804', '00805',
                               '00806', '00807', '00900', '00901', '00902', '00903', '00904', '00905', '00906',
                               '00907', '00908', '01000', '01001', '01002', '01003', '01100', '01101', '01102',
                               '01103', '01104', '01105', '01106', '01107', '01200', '01201', '01202', '01300',
                               '01301', '01302', '01300', '01301', '01302']:
            role_operation = RoleOperation(role_no=role_no, operation_code=operation_code)
            db_session.add(role_operation)
            db_session.flush()
        # 设置中断默认权限
        for trans_code in ['000000', '000010', '000090', '000060', '000110', '000020', '000130', '000150',
                           '000120', '000100', '000140', '000050', '000030', '000080', '000040', '000070']:
            terminal_trans = TerminalTransInfo(terminal_no=terminal_no, trans_code=trans_code)
            db_session.add(terminal_trans)
            db_session.flush()

        db_session.commit()
        return {'user_no': user_no, 'real_name': real_name, 'shop_name': shop_name, 'token': token}
    except Exception, e:
        print e.message
        return {}


class Captcha(MethodView):
    def get(self):
        captcha = create_captcha(draw_lines=False)
        captcha_file = 'static/captchas/%s.gif' % str(uuid.uuid4())
        captcha[0].save(captcha_file, 'GIF')

        old_captcha_file = web.ctx.session.get('captcha_file')
        if old_captcha_file and os.path.isfile(old_captcha_file):
            os.remove(old_captcha_file)
        web.ctx.session.captcha_file = captcha_file
        web.ctx.session.captcha = captcha[1]
        return "/%s" % captcha_file


class Index(MethodView):
    def get(self):
        '''
        为了配合登录后主页面的URL显示（显示http://domain.com/index而不是
        http://domain.com/login?code=******的callback地址），需要将登录过程分成两个部分：
        step 1.Login类的post方法，主要作用是设置服务器端的session会话
        step 2.从Login类的post方法redirect到本类的get方法，设置cookie内容
        '''
        if not session.get('login', None) or not session['login']:
            return render_template('login.html')
        user = db_session.query(UserInfo).filter(UserInfo.user_no==session['user_no']).one()
        real_name = user.real_name
        profile_image = '/static/profile_images/%s' % user.sina_weibo_profile_image

        q = db_session.query(RoleOperation)
        q = q.filter(RoleOperation.role_no == UserInfo.role_no)
        q = q.filter(UserInfo.user_no == session['user_no'])
        operations = '-'.join([p.operation_code for p in q.all()])
        response = make_response(render_template('admin_index.html', **locals()))
        response.set_cookie('operations', operations)
        response.set_cookie('user_no', session['user_no'])
        response.set_cookie('unit_no', session['unit_no'])
        response.set_cookie('shop_type', session['shop_type'])
        return response


class Login(MethodView):
    def __init__(self):
        self.come_from_code = '0'  # 0不是weibo用户 1新浪weibo 2腾讯weibo 3QQ号

    def get(self):
        i = request.args
        if i.get('action', '').strip() == 'register_success':
            unitno = i.get('unit_no', '').strip()
            username = i.get('user_no', '').strip()
            error = u'''注册成功，请牢记您的注册信息：</br>企业代码：%s </br>用户名：%s''' % (unitno, username)
        return render_template('login.html', success=True, **locals())

    def post(self):
        if self.come_from_code == '0':  # 0不是weibo用户 1新浪weibo 2腾讯weibo 3QQ号
            unitno = request.form['unitno']
            username = request.form['username']
            password = request.form['password']
            q = db_session.query(UserInfo).filter(and_(
                UserInfo.user_no == username,
                UserInfo.unit_no == unitno,
                UserInfo.api == self.come_from_code
            ))
        elif self.come_from_code == '1':  # sina weibo
            uid = self.username
            password = self.password
            unitno = ''  # 只在渲染模板时用
            q = db_session.query(UserInfo).filter(and_(
                UserInfo.user_no == username,
                UserInfo.api == self.come_from_code
            ))

        error = ''

        if not q.count():
            error = u'用户不存在'
            return render_template('login.html', success=False, error=error, unitno=unitno, username=username)

        user = q.one()
        if user.password != hashlib.md5(password).hexdigest():
            error = u'密码不正确'
            return render_template('login.html', success=False, error=error, unitno=unitno, username=username)

        session['login'] = True
        session['user_no'] = user.user_no
        session['is_admin'] = user.is_admin
        session['user_level'] = user.user_level
        session['unit_no'] = user.unit_no.strip()
        session['shop_no'] = user.shop_no.strip() if user.shop_no else None

        # 确定应用类型(通用OR鞋服)
        if not session['shop_no']:
            session['shop_type'] = '0'
        else:
            session['shop_type'] = db_session.query(ShopInfo).filter(ShopInfo.shop_no == session['shop_no']).one().shop_type

        # 确认默认终端
        q = db_session.query(TerminalInfo).filter(TerminalInfo.is_default == True) \
            .filter(TerminalInfo.status == '0')
        if session['shop_no']:
            q = q.filter(TerminalInfo.shop_no == session['shop_no'])
        else:
            q = q.filter(TerminalInfo.shop_no.in_(
                db_session.query(ShopInfo.shop_no).filter(ShopInfo.unit_no == session['unit_no'])))

        session['default_terminal'] = q.first().terminal_no if q.count() else None

        # 设置session商户号
        # 如果用户级别为shop或terminal,则其肯定有商户号
        if session['user_level'] in ('shop', 'terminal'):
            session['shop_no'] = user.shop_no

        # 查找默认终端
        # 集团级用户没有默认终端，需要选择其所在门店才能确认默认终端(此功能尚未实现)
        if session['user_level'] == 'shop':
            q = db_session.query(TerminalInfo)
            q = q.filter(and_(TerminalInfo.shop_no == session['shop_no'], TerminalInfo.is_default == True))
            if q.count():
                default_terminal = q.one()
                session['default_terminal'] = default_terminal.terminal_no
        return redirect('/index')  # 转到 /index 页面,此页面还有其它必须的工作


class Logout(MethodView):
    def get(self):
        session['login'] = False
        return render_template('logout.html')


class Register(MethodView):
    def get(self):
        ''' 功能：跳转到注册页面(无参数时)'''
        return render_template('/user/register.html')

    def post(self):
        ''' 提交注册 url: /user/register '''
        i = request.form
        user_no = i.get('user_no', '').strip()
        password = i.get('password', '').strip()
        repassword = i.get('repassword', '').strip()
        shop_name = i.get('shop_name', u'我的商铺').strip()
        captcha = i.get('captcha', '').strip()
        sina_weibo_uid = session.get('sina_weibo_uid', '').strip()
        sina_weibo_token = session.get('sina_weibo_token', '').strip()
        email = user_no

        # if db_session.query(UserInfo) \
        #         .filter(UserInfo.user_no == user_no).count():
        #     return render_template('/user/register.html', success=False, msg=u'此用户名已被注册', **locals())
        if not password == repassword:
            return render_template('/user/register.html', success=False, msg=u'两次输入的密码不一致', **locals())
        else:
            add_user_result = add_new(user_no, password, shop_name, email=email)
            if not add_user_result:  # 没有注册成功
                return render_template('/user/register.html', success=False, msg=u'注册失败:未知错误')

            # 注册成功，更新 weibo uid
            user = db_session.query(UserInfo).filter(UserInfo.user_no == add_user_result['user_no']).one()
            user.sina_weibo_uid = sina_weibo_uid
            user.sina_weibo_token = sina_weibo_token
            db_session.add(user)
            db_session.commit()

            # 发送激活账号的邮件
            href = "%(domain)s/user/register/check?user_no=%(user_no)s&token=%(token)s" % {
            'domain': app.config['DOMAIN'], 'user_no': user_no, 'token': add_user_result['token']}
            html = u"""<a href='%(href)s'>您的注册申请已提交，请点此完成注册</a>
                    如果不能点击此链接，请复制以下地址到浏览器地址栏并转到: %(href)s
            """ % {'href': href}

            send_email_result = MyEmail().send_email(_from=app.config['EMAIL_ACCOUNT'],
                                                     password=app.config['EMAIL_PASSWORD'], subject=u'邮箱验证', to=user_no,
                                                     content=html)
            if send_email_result:
                return render_template('/info.html', 
                                       title=u'注册成功',
                                       info=u'请登录您的邮箱,完成注册过程')
            else:
                return render_template('/info.html',
                                       title=u'注册失败',
                                       info=u'发送激活邮件失败,可能是您填写的邮箱不正确',
                                       links=[{'href': '/user/register', 'label': u'点此重新注册'}])


class RegisterCheck(MethodView):
    def get(self):
        '''验证注册信息: url: /user/register/check?user_no=[user_no]&token=[token]'''
        user_no = request.args.get('user_no', '').strip()
        token = request.args.get('token', '').strip()

        q = db_session.query(UserInfo).filter(UserInfo.user_no == user_no) 
        if not q.count():
            return render_template('/info.html',
                                   title=u'验证失败：无此用户')
        
        user = q.one()
        if not user.token == token:
            return render_template('/info.html',
                                   title=u'验证失败：校验码错，请重新注册',
                                   links=[{'href': '/user/register', 'label': u'此此重新注册'}])

        # unit = q.one()
        # if not unit.status == '2':
        #     return redirect('/user/register.html', success=False, msg=u'验证失败，集团处于禁止验证状态')
        unit_no = user.unit_no.strip()
        print 'abc'
        with engine.begin() as conn:
            conn.execute("UPDATE user_info SET status = '0' WHERE user_no = %s", (user_no,))
            conn.execute("UPDATE unit_info SET status = '0' WHERE unit_no = %s", (unit_no,))
            conn.execute("UPDATE shop_info SET status = '0' WHERE unit_no = %s", (unit_no,))
            conn.execute("UPDATE terminal_info SET status = '0' WHERE shop_no in (select shop_no from shop_info where unit_no = %s)", (unit_no,))
        print 'def'
        # db_session.query(UserInfo).filter(UserInfo.user_no == user_no) \
        #           .update({'status': '0'}, synchronize_session=False)
        # db_session.query(UnitInfo).filter(UnitInfo.unit_no == unit_no) \
        #           .update({'status': '0'}, synchronize_session=False)
        # db_session.query(ShopInfo).filter(ShopInfo.unit_no == unit.unit_no) \
        #           .update({'status': '0'}, synchronize_session=False)
        # db_session.query(TerminalInfo).filter(
        #         TerminalInfo.shop_no.in_(
        #             db_session.query(ShopInfo.shop_no).filter(ShopInfo.unit_no == unit.unit_no))) \
        #         .update({'status': '0'}, synchronize_session=False)
        # db_session.commit()
        # 发送邮件
        html = u"""
            您已成功注册聚客商铺管理系统，以下是您的注册信息</br>
            企业代码: %s </br>
            用户名：%s
        """ % (unit_no, user_no)
        print 'jkl'
        MyEmail().send_email(_from=app.config['EMAIL_ACCOUNT'],
                             password=app.config['EMAIL_PASSWORD'],
                             subject=u'邮箱验证',
                             to=user_no,
                             content=html)
        print 'ghi'
        return redirect('/?action=register_success&user_no=%s&unit_no=%s' %(user_no, unit_no))


class User(MethodView):
    @authority.permission_required('00202')
    def put(self, user_no):
        input = request.json
        user_name = input.get('real_name', '').strip()

        try:
            user = db_session.query(UserInfo).filter(
                and_(UserInfo.user_no == user_no, UserInfo.unit_no == session['unit_no'])).one()
            # 更新系统用户信息
            user.real_name = user_name
            db_session.commit()
            return jsonify(success=True, msg=rspmsg.SUCCESS)

        except Exception, e:
            return jsonify(success=False, msg=rspmsg.USER_DONOT_EXIST)

    @authority.permission_required('00202')
    def delete(self, user_no):
        q = db_session.query(UserInfo).filter(
            and_(UserInfo.user_no == user_no, UserInfo.unit_no == session['unit_no']))
        if q.count():
            status = '1' if q.one().status == '0' else '0'
            q.update({'status': status}, synchronize_session=False);
            db_session.commit()
            return jsonify(success=True, msg=u'停用系统用户成功', show_msg=True)
        else:
            return jsonify(success=False, msg=u'无此用户', show_msg=True)


class UserList(MethodView):
    @authority.permission_required('00203')
    def get(self):
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        user_no = request.args.get('user_no', '').strip()

        # 如果是：
        #   超级用户－获取所有系统用户信息
        #   集团级用户－获取此集团下的商户级用户信息
        #   商户级用户－获取此商户下的终端级用户信息

        q = db_session.query(UserInfo, UnitInfo, ShopInfo).order_by(UserInfo.user_no)
        if session['user_level'] == 'super':
            pass
        elif session['user_level'] == 'unit':
            q = q.filter(UserInfo.user_level == 'shop')
            q = q.filter(UserInfo.unit_no == session['unit_no'])
        elif session['user_level'] == 'terminal':
            q = q.filter(UserInfo.user_level == 'terminal')
            q = q.filter(UserInfo.unit_no == session['unit_no'])
            q = q.filter(UserInfo.shop_no == session['shop_no'])

        if user_no:
            q = q.filter(UserInfo.user_no == user_no)
        q = q.outerjoin(UnitInfo, UnitInfo.unit_no == UserInfo.unit_no)
        q = q.outerjoin(ShopInfo, ShopInfo.shop_no == UserInfo.shop_no)
        total = q.count()
        users = q.limit(limit).offset((page - 1) * limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit, data=[
            {'user_no': u.UserInfo.user_no,
             'real_name': u.UserInfo.real_name,
             'user_level': u.UserInfo.user_level,
             'status': u.UserInfo.status,
             'unit_no': u.UnitInfo.unit_no,
             'unit_name': u.UnitInfo.unit_name,
             'shop_no': u.ShopInfo.shop_no if u.ShopInfo else '',
             'shop_name': u.ShopInfo.shop_name if u.ShopInfo else ''} for u in users
        ])

    @authority.permission_required('00200')
    def post(self):
        user = request.json
        if db_session.query(UserInfo).filter(UserInfo.user_no == user['user_no']).count():
            return jsonify(success=False, msg=rspmsg.USER_ALREADY_EXIST)
        else:
            new_user = UserInfo(
                user_no=user['user_no'],
                real_name=user['real_name'],
                unit_no=user.get('unit_no', ''),
                password=md5('000000').hexdigest()
            )

            db_session.add(new_user)
            db_session.commit()
            return jsonify(success=True, msg=rspmsg.ADD_USER_SUCCESS)


class UserOperations(MethodView):
    # 获取当前系统用户权限
    def get(self):
        q = db_session.query(RoleOperation)
        q = q.filter(RoleOperation.role_no == UserInfo.role_no)
        q = q.filter(UserInfo.user_no == session['user_no'])
        total = q.count()
        operations = q.all()
        return jsonify(success=True, total=total,
                       data=[{'operation_code': p.operation_code} for p in operations])


class UserAccount(MethodView):
    def get(self):
        # 获取集团信息
        unit_info = db_session.query(UnitInfo).filter(UnitInfo.unit_no == session['unit_no']).one()
        user_info = db_session.query(UserInfo).filter(UserInfo.user_no == session['user_no']).one()

        return jsonify(success=True, show_msg=False,
                       data={
                           'unit_no': unit_info.unit_no,
                           'unit_type': unit_info.type,
                           'unit_create_datetime': unit_info.create_datetime.strftime('%Y/%m/%d'),
                           'shop_limit': unit_info.shop_limit,
                           'weixin_token': unit_info.weixin_token,
                           'user_no': user_info.user_no
                       })


class MyProfile(MethodView):
    def get(self):
        sql = '''
            SELECT ur.user_no, ur.real_name, ur.reg_time, un.unit_no, un.unit_name, sp.shop_no, sp.shop_name
            FROM user_info ur
            LEFT JOIN unit_info un ON ur.unit_no = un.unit_no
            LEFT JOIN shop_info sp ON ur.shop_no = sp.shop_no
            WHERE ur.user_no = %s
        '''
        user = engine.execute(sql, (session['user_no'],)).first()
        return jsonify(success=True, 
                       data=[{'user_no': user[0], 'user_name': user[1], 
                              'reg_time': user[2].strftime('%Y/%m/%d %H:%M:%S'),
                              'unit_no': user[3], 'unit_name': user[4], 'shop_no': user[5],
                              'shop_name': user[6]}])

