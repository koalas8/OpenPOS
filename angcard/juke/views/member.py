#-*- coding=utf-8 -*-

import datetime
import uuid
import hashlib
from flask import session, request, Blueprint
from flask.json import jsonify
from flask.views import MethodView
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from juke.modules import *
from juke import app
from juke import authority


class MemberCardList(MethodView):
    @authority.permission_required('01003')
    # 会员持卡信息
    def get(self, member_id):       
        if not member_id:
            return jsonify(success=False, msg=u'无效参数')

        q = db_session.query(CardInfo).filter(CardInfo.member_id==member_id).filter(CardInfo.unit_no==session['unit_no'])
        total = q.count()
        cards = q.all()
        return jsonify(success=True, total=total, page=1, limit=20,
                       data=[{'card_no': c.card_no, 'amount': c.amount, 'status': c.status} for c in cards])


class MemberList(MethodView):
    @authority.permission_required('01001')
    def get(self):
        i = request.args
        member_id = i.get('member_id', '').strip()
        card_no, member_name = i.get('card_no', '').strip(), i.get('member_name', '').strip()
        id_card, phone = i.get('id_card', '').strip(), i.get('phone', '').strip()
        page, limit = int(i.get('page', '1').strip()), int(i.get('limit', '10').strip())
        sleep_date = i.get('sleep_date', '').strip()  # 至现在没有进行交易的天数
        m = aliased(MemberInfo)
        c = aliased(CardInfo)
        q = db_session.query(c.card_no, c.custom_card_no, c.card_type, c.amount, c.total_pay, c.points, m.id, m.member_name, m.sex, m.email, m.phone)
        q = q.outerjoin(m, c.member_id == m.id)
        q = q.filter(c.unit_no == session['unit_no'])
        q = q.filter(c.member_id != None)

        if member_id:
            q = q.filter(m.id == id)
        if card_no:
            q = q.filter(or_(c.card_no == card_no), (c.custom_card_no == cardno))
        if member_name:
            q = q.filter(m.member_name == member_name)
        if id_card:
            q = q.filter(m.idcard == id_card)
        if phone:
            q = q.filter(m.phone == phone)

        if sleep_date:
            now = datetime.datetime.now()
            sleep_date = now - datetime.timedelta(days=int(sleep_date))
            q = q.filter(m.last_trans_time <= sleep_date)
        total = q.count()
        members = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit,
                        data=[{'card_no': m.card_no if m.card_type == '0' else m.custom_card_no,
                              'custom_card_no': m.custom_card_no,
                              'member_id': m.id,
                              'member_name': m.member_name,
                              'phone': m.phone,
                              'amount': m.amount,
                              'total_pay': m.total_pay,
                              'points': m.points} for m in members])

    @authority.permission_required('01000')
    def post(self):
        input = request.json
        card = input.get('card', {})
        card_no = card.get('card_no', '').strip()  # 卡号
        property_deposit = card.get('property_deposit', 't').strip() # 是否可充值
        property_times = card.get('property_times', 'f').strip()  # 是否可计次
        amount = int(card.get('amount', '0'))  # 卡内余额
        times = int(card.get('times', '0'))  # 卡内计次金额
        points = int(card.get('points', '0'))  # 卡内积分
        points_rule = float(card.get('points_rule', '0'))  #  积分规则
        exp_date = card.get('exp_date', '20151231').strip()  # 过期时间
        member_name = input.get('member_name', '').strip()
        shop_no = input.get('shop_no', '').strip()
        sex = input.get('sex', '').strip()
        idcard = input.get('idcard', '').strip()
        phone = input.get('phone', '').strip()
        birthday = input.get('birthday', '').strip()
        email = input.get('email', '').strip()
        address = input.get('address', '').strip()
        password = card.get('password', '').strip()
        repassword = card.get('repassword', '').strip()        

        if not (card_no and member_name and shop_no):
            return jsonify(success=False, msg=u'请正确填写必填项')

        if not (password == repassword):
            return jsonify(success=False, msg=u'两次输入的密码不一致')

        # 查找
        if not db_session.query(ShopInfo).filter(and_(ShopInfo.shop_no==shop_no, ShopInfo.unit_no==session['unit_no'])).count():
            return jsonify(success=False, msg=u'无此分店')

        # 下面的这个member实例可以在自发卡处理过程和系统卡处理过程中通用
        member_id = str(uuid.uuid4())
        member = MemberInfo(id=member_id, unit_no=session['unit_no'], shop_no=shop_no, member_name=member_name, 
                            sex=sex, idcard=idcard, phone=phone, birthday=birthday, email=email, address=address)
            
        if not (len(card_no)==19 and card_no.startswith('999')):  # 客户自发卡
            q = db_session.query(CardInfo).filter(CardInfo.custom_card_no==card_no)
            q = q.filter(CardInfo.unit_no==session['unit_no'])
            if q.count():
                return jsonify(success=False, msg=u'此卡已被会员持有')
            else:
                print "member.py: password ->", password
                print "member.py: password_md5 ->", hashlib.md5(password).hexdigest()

                # 以下循环是为了防止出现重复的卡号
                # sys_card_no 是为客户自发卡搭配的系统卡号                
                sys_card_no=str(uuid.uuid4()).replace('-', '')[:19]
                while db_session.query(CardInfo).filter(CardInfo.card_no==sys_card_no).count():
                    sys_card_no=str(uuid.uuid4()).replace('-', '')[:19]

                new_card = CardInfo(card_no=sys_card_no, 
                    custom_card_no=card_no, property_deposit=property_deposit, 
                    property_times=property_times, amount=amount, times=times, points=points,
                    points_rule=points_rule, exp_date=exp_date, member_id=member_id, 
                    track_2='0'*37, unit_no=session['unit_no'], valid_life=12,
                    card_type='1', password=hashlib.md5(password).hexdigest())
                
                db_session.add(member)
                db_session.flush()
                db_session.add(new_card)
                db_session.commit()
                return jsonify(success=True, msg=u'添加会员信息成功')
                
        else:  # 系统卡处理过程
            q = db_session.query(CardInfo).filter(CardInfo.card_no==card_no)
            q = q.filter(CardInfo.unit_no==session['unit_no'])

            if not q.count():
                return jsonify(success=False, msg=u'无此卡号')

            card_info = q.one()

            if card_info.member_id:
                return jsonify(success=False, msg=u'此卡已被会员持有')

            card_info.member_id = member_id
            db_session.add(card_info)
            db_session.add(member)
            db_session.commit()
            return jsonify(success=True, msg=u'添加会员信息成功')