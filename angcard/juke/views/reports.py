#-*- coding=utf-8 -*-
import datetime
from flask import session, request, Blueprint
from flask.json import jsonify
from flask.views import MethodView
from sqlalchemy import Table
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import aliased
from juke.modules import *
from juke import rspmsg
from juke import app
from juke import authority


class BalanceReport(MethodView):
    @authority.permission_required('00900')
    def get(self):
        i = request.args
        unit_no = session['unit_no']
        user_level = session['user_level']
        page, limit = int(i.get('page', 1)), int(i.get('limit', 10))

        q = db_session.query(
            func.sum(CardInfo.amount).label('amount'),
            func.sum(CardInfo.points).label('points'),
            func.count(CardInfo.card_no).label('count'),
            UnitInfo.unit_no,
            UnitInfo.unit_name
        )
        q = q.outerjoin(UnitInfo, CardInfo.unit_no == UnitInfo.unit_no)
        q = q.group_by(UnitInfo.unit_no, UnitInfo.unit_name)

        if user_level == 'unit':
            q = q.filter(UnitInfo.unit_no == unit_no)

        if user_level in ['shop', 'operator']:
            return jsonify(success=False, msg=rspmsg.PERMISSION_DENIDE)

        total = q.count()
        balances = q.limit(limit).offset((page - 1) * limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'amount': b.amount, 'points': b.points, 'count': b.count,
                              'unit_no': b.unit_no, 'unit_name': b.unit_name} for b in balances])


class UnitMxReport(MethodView):
    @authority.permission_required('00904')
    def get(self):
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=1)
        yesterday = yesterday.strftime('%Y%m%d')

        i = request.args
        trans_code = i.get('trans_code', '').strip()
        limit, page = int(i.get('limit', 10)), int(i.get('page', 1))
        trans_date = i.get('trans_date', '%s-%s' % (yesterday, yesterday)).split('-')
        start_date = trans_date[0].strip()
        end_date = trans_date[1].strip()

        if start_date[4:6] == end_date[4:6]:
            trans_table = Table('trans_' + start_date[4:6], metadata, autoload=True)
        else:
            trans_table = Trans
        ht = aliased(trans_table)
        cu = aliased(UnitInfo)
        du = aliased(UnitInfo)
        sp = aliased(ShopInfo)
        ts = aliased(Trans)
        t = aliased(TerminalTransDim)

        q_1 = db_session.query(
            ht.card_no, ht.trans_date, ht.trans_time, ht.amount,
            cu.unit_name.label('credit_unit'), du.unit_name.label('debit_unit'),
            sp.shop_name, t.trans_name)
        q_1 = q_1.outerjoin(cu, ht.credit_unit == cu.unit_no)
        q_1 = q_1.outerjoin(du, ht.debit_unit == du.unit_no)
        q_1 = q_1.outerjoin(sp, ht.shop_no == sp.shop_no)
        q_1 = q_1.outerjoin(t, ht.trans_code == t.trans_code)
        q_1 = q_1.filter(and_(ht.trans_date.between(start_date, end_date), ht.debit_unit == session['unit_no']))
        q_1 = q_1.filter(and_(ht.reversiable == '0', or_(ht.result_code == '00', ht.result_code == '0')))
        q_1 = q_1.filter(ht.trans_code == trans_code) if trans_code else q_1

        q_2 = db_session.query(
            ts.card_no, ts.trans_date, ts.trans_time, ts.amount,
            cu.unit_name.label('credit_unit'), du.unit_name.label('debit_unit'),
            sp.shop_name, t.trans_name)
        q_2 = q_2.outerjoin(cu, ts.credit_unit == cu.unit_no)
        q_2 = q_2.outerjoin(du, ts.debit_unit == du.unit_no)
        q_2 = q_2.outerjoin(sp, ts.shop_no == sp.shop_no)
        q_2 = q_2.outerjoin(t, ts.trans_code == t.trans_code)
        q_2 = q_2.filter(and_(ts.trans_date.between(start_date, end_date), ts.debit_unit == session['unit_no']))
        q_2 = q_2.filter(and_(ts.reversiable == '0', or_(ts.result_code == '00', ts.result_code == '0')))
        q_2 = q_2.filter(ts.trans_code == trans_code) if trans_code else q_2

        q = q_1.union(q_2).order_by(ts.trans_date, ts.trans_time)
        total = q.count()
        trans = q.all()

        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'card_no': t.card_no, 'trans_date': t.trans_date, 'trans_time': t.trans_time,
                              'amount': t.amount, 'credit_unit': t.credit_unit, 'debit_unit': t.debit_unit,
                              'shop_name': t.shop_name, 'trans_name': t.trans_name} for t in trans])


class ShopMxReport(MethodView):
    @authority.permission_required('00905')
    def get(self):
        i = request.args
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=1)
        yesterday = yesterday.strftime('%Y%m%d')

        limit, page = int(i.get('limit', 10)), int(i.get('page', 1))

        shop_no = i.get('shop_no', '').strip()
        trans_date = i.get('trans_date', '%s-%s' % (yesterday, yesterday)).split('-')
        start_date = trans_date[0].strip()
        end_date = trans_date[1].strip()
        trans_code = i.get('trans_code', '').strip()

        if not db_session.query(ShopInfo).filter(ShopInfo.shop_no==shop_no).filter(ShopInfo.unit_no==session['unit_no']).count():
            return jsonify(success=False, msg=u'无此商户')
        if start_date[4:6] == end_date[4:6]:
            trans_table = Table('trans_'+start_date[4:6], metadata, autoload=True)
        else:
            trans_table = Trans
        h = aliased(trans_table)
        s = aliased(ShopInfo)
        cu = aliased(UnitInfo)
        du = aliased(UnitInfo)

        q = db_session.query(
                h.card_no, h.trans_date, h.trans_time, h.amount, h.terminal_no, s.shop_name,
                cu.unit_name.label('credit_unit'), du.unit_name.label('debit_unit'))
        q = q.outerjoin(s, h.shop_no == s.shop_no)
        q = q.outerjoin(cu, h.credit_unit == cu.unit_no)
        q = q.outerjoin(du, h.debit_unit == du.unit_no)
        if trans_code:
            q = q.filter(h.trans_code==trans_code)
        q = q.filter(h.trans_date.between(start_date, end_date))
        q = q.filter(h.reversiable=='0')
        q = q.filter(or_(h.result_code=='0', h.result_code=='00'))        

        total = q.count()
        trans = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit, 
            data=[{
                'card_no': t.card_no, 'trans_date': t.trans_date, 'trans_time': t.trans_time,
                'amount': t.amount, 'credit_unit': t.credit_unit, 'debit_unit': t.debit_unit,
                'shop_name': t.shop_name, 'trans_name': t.trans_name} for t in trans])


class TerminalMxReport(MethodView):
    @authority.permission_required('00906')
    def get(self):
        i = request.args
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=1)
        yesterday = yesterday.strftime('%Y%m%d')

        terminal_no = i.get('terminal_no', '').strip()
        trans_date = i.get('trans_date', '%s-%s' % (yesterday, yesterday)).split('-')
        start_date = trans_date[0].strip()
        end_date = trans_date[1].strip()
        trans_code = i.get('trans_code', '').strip()
        page, limit = int(i.get('page', '1').strip()), int(i.get('limit', '10').strip())

        # 是否是当前集团的终端？
        shops = db_session.query(ShopInfo.shop_no).filter(ShopInfo.unit_no==session['unit_no']).all()
        q = db_session.query(TerminalInfo).filter(TerminalInfo.terminal_no==terminal_no)
        q = q.filter(TerminalInfo.shop_no.in_(shops))
        if not q.count():
            return jsonify(success=False, msg=u'无此终端')

        if start_date[4:6] == end_date[4:6]:
            trans_table = Table('trans_'+start_date[4:6], metadata, autoload=True)
        else:
            trans_table = Trans
            
        h = aliased(trans_table)
        s = aliased(ShopInfo)
        cu = aliased(UnitInfo)
        du = aliased(UnitInfo)

        q = db_session.query(h.card_no, h.trans_date, h.trans_time, h.amount, h.terminal_no, s.shop_name,
                cu.unit_name.label('credit_unit'), du.unit_name.label('debit_unit'))        
        q = q.outerjoin(s, h.shop_no == s.shop_no)
        q = q.outerjoin(cu, h.credit_unit == cu.unit_no)
        q = q.outerjoin(du, h.debit_unit == du.unit_no)
        q = q.filter(HistoryTrans.terminal_no==terminal_no)
        q = q.filter(HistoryTrans.trans_date.between(start_date, end_date))
        q = q.filter(or_(HistoryTrans.result_code=='00', HistoryTrans.result_code=='0'))
        q = q.filter(or_(HistoryTrans.reversiable=='0', HistoryTrans.reversiable=='2'))
        
        if trans_code:
            q = q.filter()
        total = q.count()
        trans = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit, 
            data=[{
                'card_no': t.card_no, 'trans_date': t.trans_date, 'trans_time': t.trans_time,
                'amount': t.amount, 'credit_unit': t.credit_unit, 'debit_unit': t.debit_unit,
                'shop_name': t.shop_name, 'trans_name': t.trans_name} for t in trans])


