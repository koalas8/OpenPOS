# encoding=utf-8

from flask import session, make_response
from flask.json import jsonify
from modules import *


# 超级用户认证
def super_required():
    def warp(func):
        def m(*args, **kwargs): 
            if not session['login']:
                response = make_response(jsonify(success=False, msg=u'您已退出系统', show_msg=True, redirect_url='/'))
                return response
            print '------> super user check: user_level -> ', session['user_level']
            if session['user_level'] == 'super':
                ret = func(*args, **kwargs)
            else:
                ret = jsonify(success=False, msg=u'您无此权限', show_msg=True)
            return ret
        return m
    return warp


# 管理员认证
def admin_required():
    def warp(func):
        def m(*args, **kwargs): 
            if not session.get('login', None) or not session['login']:
                response = make_response(jsonify(success=False, msg=u'您已退出系统', show_msg=True, redirect_url='/'))
                return response
            print '------> admin user check: user is admin -> ', session['is_admin']
            if session['is_admin']:
                ret = func(*args, **kwargs)
            else:
                ret = jsonify(success=False, msg=u'您无此权限', show_msg=True)
            return ret
        return m
    return warp


# 权限认证
def permission_required(operation_code):
    def warp(func):
        def m(*args, **kwargs):
            if not session.get('login', None) or not session['login']:
                response = make_response(jsonify(success=False, msg=u'您已退出系统', show_msg=True, redirect_url='/'))
                return response
            # print '------> permission authority'
            q = db_session.query(RoleOperation)
            q = q.filter(RoleOperation.operation_code == operation_code)
            q = q.filter(RoleOperation.role_no == UserInfo.role_no)
            q = q.filter(UserInfo.user_no == session['user_no'])
            if q.count() > 0:
                ret = func(*args, **kwargs)
            else:
                ret = jsonify(success=False, msg=u'您无此权限', show_msg=True)
            return ret

        return m

    return warp
