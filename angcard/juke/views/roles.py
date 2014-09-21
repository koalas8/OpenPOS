#-*- coding=utf-8 -*-
import uuid
from flask import session, request, Blueprint
from flask.json import jsonify
from flask.views import MethodView
from sqlalchemy import and_
from juke.modules import *
from juke import app
from juke import authority


class RoleList(MethodView):
    @authority.permission_required('00102')
    def get(self):
        i = request.args
        role_no = i.get('role_no', '').strip()
        page, limit = int(i.get('page', '1').strip()), int(i.get('limit', '10').strip())
        if role_no:
            q = db_session.query(RoleInfo).filter(RoleInfo.role_no==role_no)
            if not q.count():
                return jsonify(success=False, msg=u'权限不存在')
            else:
                role = q.one()
                q = db_session.query(RoleOperation.operation_no, SysOperationDim.operation_name)
                q = q.outerjoin(SysOperationDim, RoleOperation.operation_no==SysOperationDim.operation_no)
                q = q.filter(RoleOperation.role_no==role_no)
                total = q.count()
                operations = q.limit(limit).offset((page-1)*limit).all()
                operations = [{'operation_no': o.operation_no, 'operation_name': o.operation_name} for o in operations]
                return jsonify(success=True, total=total, page=page, limit=limit,
                    data=[{'role_name': role_name, 'operations': operations}])
        else:
            q = db_session.query(RoleInfo).filter(RoleInfo.unit_no==session['unit_no'])
            total = q.count()
            roles = q.limit(limit).offset((page-1)*limit).all()
            return jsonify(success=True, total=total, page=page, limit=limit,
                data=[{'role_no': r.role_no, 'role_name': r.role_name} for r in roles])

    @authority.admin_required()
    @authority.permission_required('00100')
    def post(self):
        i = request.json
        role_name = i.get('role_name', '').strip()
        operations = i.get('operations', [])
        if not role_name:
            return jsonify(success=False, msg=u'请输入权限内容')
        if not operations:
            return jsonify(success=False, msg=u'请选择权限内容')

        role_no = str(uuid.uuid4())
        role = RoleInfo(role_no=role_no, role_name=role_name, creator=session['user_no'], unit_no=session['unit_no'])
        db_session.add(role)
        db_session.flush()

        role_content_count = 0
        for operation in operations:
            if db_session.query(SysOperationDim).filter(SysOperationDim.operation_code==operation).count():
                role_content = RoleOperation(operation_code=operation, role_no=role_no)
                db_session.add(role_content)
                role_content_count += 1
        if role_content_count:
            db_session.commit()
            return jsonify(success=True, msg=u'添加权限成功')
        else:
            db_session.rollback()
            return jsonify(success=False, msg=u'添加权限失败: 无权限内容')


class RoleGrantList(MethodView):
    @authority.permission_required('00105')
    def get(self):
        i = request.args
        page, limit = int(i.get('page', '1').strip()), int(i.get('limit', '10').strip())
        q = db_session.query(UserInfo.user_no, UserInfo.real_name, RoleInfo.role_name).outerjoin(RoleInfo, UserInfo.role_no==RoleInfo.role_no)
        q = q.filter(UserInfo.unit_no==session['unit_no'])
        total = q.count()
        grant_list = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit,
            data=[{'user_no': g.user_no, 'real_name': g.real_name, 'role_name': g.role_name} for g in grant_list])

    @authority.permission_required('00103')
    def post(self):
        i = request.json
        unit_no, user_no, role_no = i.get('unit_no', '').strip(), i.get('user_no', '').strip(), i.get('role_no', '').strip()
        if not user_no: 
            return jsonify(success=False, msg=u'请选择用户')
        if not role_no: 
            return jsonify(success=False, msg=u'请选择权限')

        q_user = db_session.query(UserInfo).filter(UserInfo.user_no==user_no)
        q_user = q_user.filter(UserInfo.unit_no==unit_no)
        if not q_user.count(): 
            return jsonify(success=False, msg=u'用户不存在')
        q_role = db_session.query(RoleInfo).filter(and_(RoleInfo.role_no==role_no, RoleInfo.unit_no==unit_no))
        if not q_role.count(): 
            return jsonify(success=False, msg=u'权限不存在')

        q_user.update({'role_no': role_no})
        db_session.commit()
        return jsonify(success=True, msg=u'授权成功')


class RoleOperations(MethodView):
    # 获取当前用户可以进行设置的后台功能
    def get(self):
        _type = request.args.get('type', '').strip()
        role_id = request.args.get('role_id', '').strip()

        if not role_id:
            return jsonify(success=False, msg=u'请设置RoleId参数', show_msg=True)

        q = db_session.query(SysOperationDim.operation_code, SysOperationDim.operation_name, 
                             SysOperationType.type_code, SysOperationType.type_name)
        q = q.outerjoin(SysOperationType, SysOperationDim.operation_type_code==SysOperationType.type_code)
        if session['user_level'] == ['unit']:
            q = q.filter(SysOperationDim.unit_level==True)
        elif session['user_level'] == ['shop']:
            q = q.filter(SysOperationDim.shop_level==True)
        elif session['user_level'] == ['terminal']:
            q = q.filter(SysOperationDim.terminal_level==True)
        if role_id:
            q = q.outerjoin(RoleOperation, SysOperationDim.operation_code==RoleOperation.operation_code)
            q = q.filter(RoleOperation.role_id==role_id)
        operations = q.all()
        total = q.count()
        
        data = []  # data = [{'type_code': '', 'type_name': '', 'operations': [{'operation_code': '', 'operation_name': ''}]}]
        if type=='tree':
            for p in operations:
                _type_code_in_data = False
                for d in data:
                    if p.type_code == d['type_code']:
                        _type_code_in_data = True
                        d['operations'].append({'operation_code': p.operation_code, 'operation_name': p.operation_name})
                        break
                if not _type_code_in_data:
                    data.append({'type_code': p.type_code, 'type_name': p.type_name, 'operations': [{'operation_code': p.operation_code, 'operation_name': p.operation_name}]})
        else:
            data = [{'operation_code': p.operation_code, 'operation_name': p.operation_name} for p in operations]
        return jsonify(success=True, total=total, page=1, limit=9999, data=data)