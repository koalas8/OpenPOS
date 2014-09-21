#-*- coding=utf-8 -*-
import uuid
from flask import session, request, Blueprint
from flask.json import jsonify
from flask.views import MethodView
from sqlalchemy import and_
from juke.modules import *
from juke.libs import wechat
from juke import app
from juke import authority


class Token(MethodView):
    def get(self):
        q = db_session.query(UnitInfo).filter(UnitInfo.unit_no == session['unit_no'])
        if not q.count():
            return jsonify(success=False, token="", msg=u'没有找到token', show_msg=False)
        else:
            q = q.one()
            return jsonify(success=True, token=q.weixin_token)

    def post(self):
        i = request.json
        token = i.get('token', '').strip()
        if token == '':
            return jsonify(success=False, msg=u'Token不能为空')