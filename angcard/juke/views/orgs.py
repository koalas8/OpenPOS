#-*- coding=utf-8 -*-
import uuid
import random
from flask import session, request, Blueprint
from flask.json import jsonify
from flask.views import MethodView
from sqlalchemy import or_, and_
from sqlalchemy.orm import aliased
from juke.modules import *
from juke import rspmsg
from juke import app
from juke import authority


class Unit(MethodView):
    @authority.permission_required('00401')
    def put(self, unit_no):
        unit_name = request.json.get('unit_name').strip()   
        status = request.json.get('status', '0').strip()

        if session['user_level'] == 'super' or (session['unit_no']  == unit_no and session['user_level'] == 'unit'):
            unit = db_session.query(UnitInfo).filter(UnitInfo.unit_no == unit_no).one()
            unit.unit_name = unit_name
            unit.status = status
            db_session.add(unit)
            db_session.commit()
            return jsonify(success=True, msg=u'更新集团信息成功')
        else:
            return jsonify(success=False, msg=u'您不是此集团的管理员')

    @authority.super_required()
    @authority.permission_required('00401')
    def delete(self, unit_no):
        q = db_session.query(UnitInfo).filter(UnitInfo.unit_no==unit_no)
        if q.count() > 0:
            status = '1' if q.one().status == '0' else '0'
            msg = u'启用集团成功' if status == '0' else u'停用集团成功'
            q.update({'status': status})
            db_session.commit()
            return jsonify(success=True, msg=msg)
        else:
            return jsonify(success=False, msg=u'无此集团')


class UnitList(MethodView):
    @authority.permission_required('00402')
    def get(self):
        unit_no = request.args.get('unit_no', '').strip()
        page, limit = int(request.args.get('page', 1)), int(request.args.get('limit', 10))
        q = db_session.query(UnitInfo).order_by(UnitInfo.unit_no)
        if unit_no:
            q = q.filter(UnitInfo.unit_no == unit_no)
        if session['user_level'] in ['unit', 'shop']:
            q = db_session.query(UnitInfo).filter(UnitInfo.unit_no == session['unit_no'])
        if session['user_level'] == ['super']:
            q = db_session.query(UnitInfo)

        total = q.count()
        units = q.all()
        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'unit_no': u.unit_no, 'unit_name': u.unit_name, 'status': u.status} for u in units])

    @authority.super_required()
    @authority.permission_required('00400')
    def post(self):
        unit_no = request.json.get('unit_no').strip()
        unit_name = request.json.get('unit_name').strip()

        if db_session.query(UnitInfo).filter(UnitInfo.unit_no == unit_no).count():
            return jsonify(success=False, msg=rspmsg.UNIT_ALREADY_EXIST)

        unit_name = unit_name if unit_name else unit_no
        weixin_token = ''.join(random.sample(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                                              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                              'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                                              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                                              '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 32))
        unit = UnitInfo(unit_no=unit_no, unit_name=unit_name, status='0', weixin_token=weixin_token)
        db_session.add(unit)
        db_session.commit()

        return jsonify(success=True, msg=rspmsg.ADD_UNIT_SUCCESS)


class UnitInter(MethodView):
    @authority.super_required()
    @authority.permission_required('00701')
    def delete(self, inter_id):
        q = db_session.query(InterInfo).filter(InterInfo.id==inter_id)
        if q.count():
            status = '0' if q.one().status == '1' else '1'
            msg = u'启用互通成功' if status == '0' else u'停用互通成功'
            q = q.update({'status': status})
            db_session.commit()
        return jsonify(success=True, msg=msg, show_msg=True)


class UnitInterList(MethodView):
    @authority.super_required()
    @authority.permission_required('00700')
    def post(self):
        input = request.json
        credit_unit, debit_unit, remark = input.get('credit_unit', '').strip(), input.get('debit_unit', '').strip(), input.get('remark', '').strip()
        if credit_unit and debit_unit:
            if not session['user_no']:
                return rspmsg.PERMISSION_DENIDE

            if credit_unit == debit_unit:
                return jsonify(success=False, msg=u'同一集团不能互通')

            if db_session.query(InterInfo).filter(and_(
                InterInfo.credit_unit==credit_unit, InterInfo.debit_unit==debit_unit)).count() > 0:
                return simple_json_result(False, '两集团已是互通关系')

            inter_info = InterInfo(id=str(uuid.uuid4()), credit_unit=credit_unit, debit_unit=debit_unit, remark=remark)
            db_session.add(inter_info)
            db_session.commit()
            return jsonify(success=True, msg=u'添加集团互通成功')
        else:
            return jsonify(success=False, msg=u'表单错误')

    @authority.permission_required('00702')
    def get(self):
        input = request.args
        page, limit = int(input.get('page', 1)), int(input.get('limit', 10))

        cu = aliased(UnitInfo)
        du = aliased(UnitInfo)

        q = db_session.query(InterInfo.id, InterInfo.credit_unit, InterInfo.debit_unit,
                             InterInfo.status, cu.unit_name.label('credit_unit'), du.unit_name.label('debit_unit'))
        q = q.order_by(InterInfo.credit_unit)
        q = q.outerjoin(cu, cu.unit_no == InterInfo.credit_unit)
        q = q.outerjoin(du, du.unit_no == InterInfo.debit_unit)
        q = q.filter(or_(InterInfo.credit_unit == session['unit_no'], InterInfo.debit_unit == session['unit_no']))
        total = q.count()
        q = q.limit(limit).offset((page - 1) * limit)
        inter_info = q.all()

        return jsonify(success=True, total=total, limit=limit, page=page,
                       data=[{'id': i.id, 'credit_unit': i.credit_unit, 'debit_unit': i.debit_unit, 'status': i.status}
                             for i in inter_info])


class ShopList(MethodView):
    @authority.permission_required('00502')
    def get(self):
        input = request.args
        unit_no = input.get('unit_no', '').strip()
        unit_no = unit_no if unit_no else session['unit_no']
        page, limit = int(input.get('page', 1)), int(input.get('limit', 10))
        q = db_session.query(ShopInfo).order_by(ShopInfo.shop_no)
        q = q.filter(ShopInfo.unit_no == unit_no)
        total = q.count()
        shops = q.limit(limit).offset((page-1)*limit).all()

        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'shop_no': s.shop_no, 'shop_name': s.shop_name, 'status': s.status} for s in shops])

    @authority.super_required()
    @authority.permission_required('00500')
    def post(self):
        input = request.json
        shop_name, remark = input.get('shop_name', ''), input.get('remark', '')
        unit_no, shop_no = input.get('unit_no', '').strip(), input.get('shop_no', '').strip()

        if not db_session.query(UnitInfo).filter(UnitInfo.unit_no == unit_no).count():
            msg = u'所属集团不存在'
        if db_session.query(ShopInfo).filter(ShopInfo.shop_no == shop_no).count():
            msg = u'此商户号已存在'
        else:
            try:
                shop = ShopInfo(shop_no=shop_no, shop_name=shop_name, unit_no=unit_no, remark=remark)
                db_session.add(shop)
                db_session.commit()
            except Exception, e:
                print e.message
                msg = u'未知错误'
        success, msg = (True, u'添加商户成功') if not 'msg' in dir() else (False, msg)
        return jsonify(success=success, msg=msg, show_msg=True)


class Shop(MethodView):    
    @authority.permission_required('00501')            
    def delete(self, shop_no):
        q = db_session.query(ShopInfo).filter(ShopInfo.shop_no==shop_no)
        if session['user_level'] == 'super':
            pass
        elif session['user_level'] == 'unit':
            q = q.filter(ShopInfo.unit_no==session['unit_no'])
        else:
            return jsonify(success=False, msg=u'您无此权限', show_msg=True)

        if q.count():
            status = '1' if q.one().status == '0' else '0'
            msg = u'启用商户成功' if status == '0' else u'停用商户成功'
            q.update({'status': status})
            db_session.commit()
            return jsonify(success=True, msg=msg, show_msg=True)
        else:
            return jsonify(success=False, msg=u'无此商户', show_msg=True)

    @authority.permission_required('00501')
    def put(self, shop_no):
        input = request.json
        shop_name, remark = input.get('shop_name', ''), input.get('remark', '')

        q = db_session.query(ShopInfo).filter(and_(ShopInfo.shop_no == shop_no, ShopInfo.unit_no == unit_no))
        if not q.count():
            return jsonify(success=False, msg=u'无此商户', show_msg=True)
        if q.one():
            q.update({'shop_name': shop_name, 'remark': remark})
            return jsonify(success=False, msg=u'修改成功')


class Terminal(MethodView):
    # @authority.permission_required('00601')
    # def put(self):
    #     i = request.json
    #     shop_no = i.get('shop_no', '').strip()
    #     terminal_no = i.get('terminal_no', '').strip()
    #     is_default = bool(i.get('is_default', ''))
    #     remark, trans_codes = i.get('remark', ''), i.get('trans_codes', [])

    @authority.permission_required('00601')
    def delete(self, terminal_no):
        q = db_session.query(TerminalInfo).filter(TerminalInfo.terminal_no==terminal_no)        
        if session['user_level'] == 'super':
            pass
        elif session['user_level'] == 'unit':
            q = q.filter(TerminalInfo.shop_no.in_(db_session.query(ShopInfo).filter(ShopInfo.unit_no==session['unit_no'])))
        elif session['user_level'] == 'shop':
            q = q.filter(TerminalInfo.shop_no==sessiion['shop_no'])
        else:
            return jsonift(success=False, msg=u'您无此权限', show_msg=True)

        if q.count():
            status = '0' if q.one().status == '1' else '1'
            msg = u'启用终端成功' if status == '0' else u'停用终端成功'
            q.update({'status': status})
            db_session.commit()
            return jsonify(success=True, msg=msg, show_msg=True)
        else:
            return jsonify(success=False, msg=u'无此终端', show_msg=True)            


class TerminalList(MethodView):
    @authority.permission_required('00602')
    def get(self):
        input = request.args
        shop_no, terminal_no = input.get('shop_no', '').strip(), input.get('terminal_no', '').strip()
        page, limit = int(input.get('page', 1)), int(input.get('limit', 20))

        q = db_session.query(TerminalInfo.terminal_no, TerminalInfo.status, ShopInfo.shop_name, UnitInfo.unit_name)
        q = q.order_by(TerminalInfo.terminal_no)
        q = q.outerjoin(ShopInfo, TerminalInfo.shop_no == ShopInfo.shop_no)
        q = q.outerjoin(UnitInfo, ShopInfo.unit_no == UnitInfo.unit_no)
        q = q.filter(UnitInfo.unit_no == session['unit_no'])
        if shop_no:
            q = q.filter(ShopInfo.shop_no == shop_no)
        if terminal_no:
            q = q.filter(TerminalInfo.terminal_no == terminal_no)

        total = q.count()
        terminals = q.limit(limit).offset((page - 1) * limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'terminal_no': t.terminal_no, 'shop_name': t.shop_name, 'unit_name': t.unit_name,
                              'status': t.status} for t in terminals])

    @authority.permission_required('00600')
    def post(self):
        i = request.json
        shop_no = i.get('shop_no', '').strip()
        terminal_no = i.get('terminal_no', '').strip()
        is_default = bool(i.get('is_default', ''))
        remark, trans_codes = i.get('remark', ''), i.get('trans_codes', [])

        if db_session.query(TerminalInfo).filter(TerminalInfo.terminal_no == terminal_no).count():
            return jsonify(success=False, msg=rspmsg.TERMINAL_ALREADY_EXIST)

        if is_default:  # 取消原来的默认终端
            db_session.query(TerminalInfo).filter(TerminalInfo.shop_no == shop_no).update({'is_default': 'f'})

        terminal = TerminalInfo(terminal_no=terminal_no, batch_no=1, trace_no=1, shop_no=shop_no, remark=remark,
                                is_default=is_default)
        db_session.add(terminal)
        db_session.flush()
        if trans_codes:
            for t in trans_codes:
                terminal_trans = TerminalTransInfo(id=str(uuid.uuid4()), trans_code=t, terminal_no=terminal_no)
                db_session.add(terminal_trans)
        db_session.commit()
        return jsonify(success=True, msg=u'添加终端成功')


class TerminalTransCodes(MethodView):
    def get(self):
        q = db_session.query(TerminalTransDim)
        return jsonify(success=True, data=[{'trans_code': t.trans_code, 'trans_name': t.trans_name} for t in q.all()])