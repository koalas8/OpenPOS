#-*- coding=utf-8 -*-
import datetime
import uuid
from flask import session, request
from flask.json import jsonify
from flask.views import MethodView
from juke.modules import *
from sqlalchemy import and_
from juke import app
from juke import authority
from juke import rspmsg


def is_sys_card(card_no):
    card_no = str(card_no)
    if len(card_no) == 19 and card_no.startswith(app.config['CARD_BIN']) and card_no.isdigit():
        return True
    return False


class Card(MethodView):    
    @authority.permission_required('00800')
    def get(self, card_no):
        input = request.args        
        page, limit = int(input.get('page', 1)), int(input.get('limit', 10))
        # 构建查询
        q = db_session.query(CardInfo).filter(CardInfo.unit_no == session['unit_no']).order_by(CardInfo.card_no)
        if card_no:
            q = q.filter(CardInfo.card_no == card_no)
        else:            
            card_no = input.get('card_no', '').strip()
            if card_no:
                q = q.filter(CardInfo.card_no.like('%'+card_no+'%'))
        total = q.count()
        cards = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit, 
            data=[{'card_no': c.card_no, 'status': c.status, 'amount': c.amount, 
                   'points_rule': c.points_rule, 'points': c.points, 'exp_date': c.exp_date, 
                   'valid_life': c.valid_life} for c in cards])

    @authority.permission_required('00801')
    def put(self, card_no):
        input = request.json
        action = input.get('action', '').strip()
        q = db_session.query(CardInfo).filter(CardInfo.unit_no==session['unit_no'])
        if is_sys_card(card_no):
            q = q.filter(CardInfo.card_no == card_no)
        else:
            q = q.filter(CardInfo.custom_card_no == card_no)
        if not q.count():
            return jsonify(success=False, msg=u'无此卡号')

        cards = q.all()
        card_info = cards[0]
        if action == 'frozen':
            if card_info.status in ('0', '1'):
                card_info.pre_status = card_info.status
                card_info.status = '3'
                db_session.add(card_info)
                db_session.commit()
                return jsonify(success=True, msg=u'卡%s冻结成功' % card_no, 
                    data=[{'card_no': c.card_no, 'status': c.status, 'amount': c.amount, 
                           'points_rule': c.points_rule, 'points': c.points, 
                           'exp_date': c.exp_date, 'valid_life': c.valid_life} for c in cards])
            else:
                return jsonify(success=False, msg=u'非未启用卡或非正常卡不能冻结')
        elif action == 'unfrozen':
            if card_info.status in ('0', '1'):
                pass
            else:
                card_info.status = card_info.pre_status
                card_info.pre_status = ''
                db_session.add(card_info)
                db_session.commit()
            return jsonify(success=True, msg=u'卡%s解冻成功' % card_no,
                           data=[{'card_no': c.card_no, 'status': c.status, 'amount': c.amount,
                                  'points_rule': c.points_rule, 'points': c.points,
                                  'exp_date': c.exp_date, 'valid_life': c.valid_life} for c in cards])


class CardList(MethodView):
    @authority.permission_required('00800')
    def get(self):
        input = request.args
        page, limit = int(input.get('page', 1)), int(input.get('limit', 10))
        # 构建查询
        q = db_session.query(CardInfo).filter(CardInfo.unit_no == session['unit_no']).order_by(CardInfo.card_no)
        total = q.count()
        cards = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'card_no': c.custom_card_no or c.card_no, 'status': c.status, 'amount': c.amount,
                              'points_rule': c.points_rule, 'points': c.points, 'exp_date': c.exp_date,
                              'valid_life': c.valid_life} for c in cards])

    # def post(self):
    #     ''' 添加用户自发卡 '''
    #     i = request.json
    #     start_no, end_no = i.get('start_no', '').strip(), i.get('end_no', '').strip()
    #     amount, times = i.get('amount', '').strip(), i.get('times', '').strip()
    #     exp_date = i.get('exp_date', '').strip()
    #     points, points_rule = i.get('points', '').strip(), i.get('points_rule', '').strip()

    #     # 二磁道统一使用76个“0”填充。

    #     if not (start_no.isnumeric() and len(start_no)<=10 and len(start_no)>=1 and (not start_no.startswith('0'))):
    #         return jsonify(success=False, msg=u'起始卡号不正确：卡号应由数字组成且最小1位，最大10位长度。')

    #     if not end_no:  # 如果没有获取到end_no,则认为只添加一张卡，即起始卡号与终止卡号相同
    #         end_no = start_no

    #     if not (end_no.isnumeric() and len(end_no)<=10 and len(end_no)>=1 and (not end_no.startswith('0'))):
    #         return jsonify(success=False, msg=u'终止卡号不正确：卡号应由数字组成且最小1位，最大10位长度。')

    #     start_no = int(start_no)
    #     end_no = int(end_no)
    #     if end_no - start_no > 499:  # 每次最多添加500张卡
    #         return jsonify(success=False, msg=u'每次最多添加500张卡')

    #     if not amount.isnumeric():
    #         return jsonify(success=False, msg=u'余额不正确')
    #     else:
    #         amount = abs(int(amount)) * 100

    #     if not times.isnumeric():
    #         return jsonify(success=False, msg=u'计次余额不正确')

    #     exp_date = exp_date.replace('-', '').replace('/', '').replace(' ', '')
    #     if not (exp_date.isnumeric() and len(exp_date)==8):
    #         return jsonify(success=False, msg=u'有效期不正确')

    #     if not points.isnumeric():
    #         return jsonify(success=False, msg=u'积分余额不正确')

    #     if not points_rule.isnumeric():
    #         return jsonify(success=False, msg=u'积分规则不正确')

    #     cards_not_in_db = []  # 卡号未在数据库中存在
    #     cards_in_db = []  # 卡号已在数据库中存在

    #     while start_no <= end_no:
    #         if db_session.query(CardInfo).filter(and_(CardInfo.card_no==card_no, CardInfo.unit_no==session['unit_no'])).count():
    #             cards_in_db.push(card_no)
    #             continue

    #         card = {
    #             'card_no': card_no,
    #             'amount': amount,
    #             'times': times,
    #             'func_times': True,
    #             'exp_date': exp_date,
    #             'password': '670b14728ad9902aecba32e22fa4f6bd',
    #             'points': points,
    #             'points_rule': points_rule,
    #             'track_2': '0' * 76,
    #             'unit_no': session['unit_no'],
    #             'valid_life': 12
    #         }
    #         cards.push(card)
    #         start_no += 1


class CardTrans(MethodView):
    @authority.permission_required('00802')
    def get(self, card_no):
        today = datetime.datetime.today()
        yesterday = (today - datetime.timedelta(days=1)).strftime('%Y%m%d')        

        input = request.args
        limit, page = int(input.get('limit', 10)), int(input.get('page', '1'))
        card_no = input.get('card_no', '').strip()  # 卡号
        trans_code = input.get('trans_code', '').strip()  # 交易类型
        start_date = input.get('start_date', yesterday).strip().replace('-', '')  # 交易开始日期
        end_date = input.get('end_date', yesterday).strip().replace('-', '')  # 交易结束日期

        if not card_no: return jsonify(success=False, msg=rspmsg.INVALID_CARD_NO)

        card_no = '%' + card_no + '%'
        q = db_session.query(HistoryTrans.card_no, HistoryTrans.trans_date, HistoryTrans.trans_time, 
            TerminalTransDim.trans_name, TerminalRetcodeDim.result_message)
        q = q.outerjoin(TerminalTransDim, HistoryTrans.trans_code==TerminalTransDim.trans_code)
        q = q.outerjoin(TerminalRetcodeDim, HistoryTrans.result_code==TerminalRetcodeDim.result_code)
        q = q.filter(HistoryTrans.card_no.like(card_no)).filter(HistoryTrans.trans_date.between(start_date, end_date))
        if trans_code: q = q.filter(HistoryTrans.trans_code==trans_code)        

        total = q.count()
        trans = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'card_no': t.card_no, 'trans_date': t.trans_date, 'trans_time': c.trans_time,
                              'trans_name': c.trans_name, 'return_message': c.return_message} for t in trans])


class CardGroup(MethodView):
    @authority.permission_required('00805')
    def put(self, group_id):
        input = request.json
        start_card_no = input.get('start_card_no', '').strip()
        end_card_no = input.get('end_card_no', '').strip()
        group_id = input.get('group_id', '').strip()

        if not start_card_no:
            return jsonify(success=False, msg=u'起始卡号不能为空')        
        if not end_card_no:
            return jsonify(success=False, msg=u'终止卡号不能为空')
        if not group_id:
            return jsonify(success=False, msg=u'卡分组名称不能为空')
        if not len(start_card_no) == 18 or start_card_no[3:7] != session['unit_no']:
            return jsonify(success=False, msg=u'起始卡号不正确')
        if not len(end_card_no) == 18 or end_card_no[3:7] != session['unit_no']:
            return jsonify(success=False, msg=u'结束卡号不正确')
        if int(end_card_no) < int(start_card_no):
            return jsonify(success=False, msg=u'起始卡号不能大于终止卡号')

        db_session.query(CardInfo). \
            filter(and_(CardInfo.card_no.between(start_card_no, end_card_no), CardInfo.unit_no==session['unit_no'])). \
            update({CardInfo.group_id: group_id}, synchronize_session=False)
        db_session.commit()
        return jsonify(success=True, msg=u'设置卡组成功')


class CardGroupList(MethodView):
    @authority.permission_required('00806')
    def get(self):
        input = request.args
        group_id = input.get('group_id', '').strip()
        keyword = input.get('keyword', '').strip()
        page = int(input.get('page', '1').strip())
        limit = int(input.get('limit', '10').strip())

        q = db_session.query(CardGroupInfo).filter(CardGroupInfo.unit_no == session['unit_no'])
        if keyword:
            keyword = '%' + keyword + '%'
            q = q.filter(CardGroupInfo.group_name.like(keyword))
        if group_id:
            q = q.filter(CardGroupInfo.id == group_id)
        total = q.count()
        card_groups = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, total=total, page=1, limit=limit,
                       data=[{'id': c.id, 'group_name': c.group_name, 'status': c.status} for c in card_groups])

    @authority.permission_required('00804')
    def post(self):
        ''' 添加卡分组 '''
        input = request.json
        group_name = input.get('group_name', '').strip()
        if not group_name:
            return jsonify(success=False, msg=u'卡分组名称不能为空')
        card_group = CardGroupInfo(id=str(uuid.uuid4()), group_name=group_name, unit_no=session['unit_no'], status='0', creator=session['user_no'])
        db_session.add(card_group)
        db_session.commit()
        return jsonify(success=True, msg=u'添加卡组成功')