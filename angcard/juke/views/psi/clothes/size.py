# -*- encoding=utf-8 -*-

import uuid
from flask import session
from flask import request
from flask.views import MethodView
from flask.json import jsonify
from juke.modules import *


def _get_by_name(group_name):
    q = db_session.query(ClothesSizeGroupInfo).filter(ClothesSizeGroupInfo.group_name == group_name)
    if session['user_level'] == 'unit':
        q = q.filter(ClothesSizeGroupInfo.unit_no == session['unit_no'])
    if session['user_level'] == 'shop':
        q = q.filter(ClothesSizeGroupInfo.shop_no) == session['shop_no']
    return q.all()


class SizeGroupList(MethodView):
    def get(self):
        i = request.args
        page = int(i.get('page')) if i.get('page').isdigit() else 1
        limit = int(i.get('limit')) if i.get('limit').isdigit() else 10
        q = db_session.query(ClothesSizeGroupInfo)
        if session['user_level'] == 'unit':
            q = q.filter(ClothesSizeGroupInfo.unit_no == session['unit_no'])
        if session['user_level'] == 'shop':
            q = q.filter(ClothesSizeGroupInfo.shop_no) == session['shop_no']

        total = q.count()
        size_group_list = q.limit(limit).offset((page - 1) * limit).all()
        return jsonify(success=True, total=total, limit=limit, offset=offset,
                       data=[{'id': s.id, 'group_name': s.group_name} for s in size_group_list])

    def post(self):
        i = request.json
        group_name = i.get('group_name', '').strip()
        size_values = i.get('content', '').strip().split('\n')        
        
        if not group_name:
            return jsonify(success=False, msg=u'请填写分组名称', show_msg=True)
        if not size_values:
            return jsonify(success=False, msg=u'您没有填写详细的尺寸信息', show_msg=True)
        if _get_by_name(group_name):
            return jsonify(success=False, msg=u'此分组名称已存在', show_msg=True)

        size_group_id = str(uuid.uuid4())  # clothes_size_group, clothes_size_group_detail两个表要用到
        size_group = ClothesSizeGroupInfo()  
        size_group.id = size_group_id 
        size_group.group_name = group_name
        size_group.unit_no = session['unit_no']
        size_group.shop_no = session['shop_no']
        db_session.add(size_group)
        db_session.flush()

        for value in size_values:
            size = ClothesSizeGroupDetail()
            size.group_id = size_group_id
            size.size = value
            db_session.add(size)
        db_session.commit()

        return jsonify(success=True, msg=u'添加尺寸分组成功', show_msg=True)

