#-*- coding=utf-8 -*-
import datetime
import uuid
from flask import session, request
from flask import Blueprint
from flask import json
from flask.json import jsonify
from flask.views import MethodView
from sqlalchemy import and_, func
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import asc, desc
from juke.ccard.protocols.trans.Trans_pb2 import Trans as BufferTrans
from juke.ccard.globals.code_dim import get_result_message
from juke.modules import *
from juke import app
from juke import authority


# 订单/小票列表
class OrderList(MethodView):
    @authority.permission_required('01105')
    def get(self):
        # 获取订单列表
        i = request.args
        order_id = i.get('order_id', '').strip()
        page, limit = int(i.get('page', '1')), int(i.get('limit', '10'))

        q = db_session.query(SaleOrderInfo).filter(SaleOrderInfo.unit_no == session['unit_no'])
        if order_id:
            q = q.filter(SaleOrderInfo.id == order_id)
        else:
            q = q.filter(SaleOrderInfo.is_paid == True)
        q = q.order_by(desc(SaleOrderInfo.create_time))
        total = q.count()
        orders = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'id': d.id, 'goods_amount': d.goods_amount, 'amount': d.amount,
                              'create_time': d.create_time.strftime('%Y/%m/%d  %H:%M:%S'), 'is_paid': d.is_paid,
                              'card_pay_amount': d.card_pay_amount, 'cash_pay_amount': d.cash_pay_amount,
                              'mode_of_payment': d.mode_of_payment} for d in orders])

    @authority.permission_required('01104')
    def post(self):
        # 生成商品订单
        # 参数格式:
        #   {"order":
        #       [
        #           {"goods_id":"add714d9-2a0b-4314-bb26-373c0ab15de2",
        #            "goods_name":"asdf",
        #            "price":25,
        #            "sale_price":0,
        #            "goods_amount":1,
        #            "money_amount":25,
        #            "discounted_money_amount":15,
        #            "discount":"60"
        #            }
        #        ]
        #    }
        i = request.json
        order = i.get('order', [])
        if not order:
            return jsonify(success=False, msg=u'提交的订单中没有商品')

        order_goods_counts = {}  # order中每种商品的数量，格式为 {goods_id: goods_amount, goods_id: goods_amount, ...}
        purchase_price = {}  # order中每种商品的采购价，格式为 {goods_id: price, goods_id: price, ...}
        goods_ids = []  # order中所有商品的ID，此中的值是唯一的
        goods_amount = 0  # order中所有商品的数量
        profit = 0  # 此订单的利润
        payment_amount = 0  # 此订单支付总额
        sale_order_details = []
        goods_not_enough = []  # 库存不足的商品
        order_id = str(uuid.uuid4())

        # 回收未支付订单的库存


        # 整理数据
        for g in order:
            if not g['goods_id'] in order_goods_counts.keys():
                order_goods_counts[g['goods_id']] = int(g['goods_amount'])
            else:
                order_goods_counts['goods_id'] += int(g['goods_amount'])

        goods_ids = order_goods_counts.keys()
        q = db_session.query(GoodsInfo).filter(GoodsInfo.id.in_(goods_ids))

        # 检查是否是当前集团的商品
        if q.count() != len(goods_ids):
            q = db_session.query(GoodsInfo.id, GoodsInfo.goods_name)
            q = q.filter(and_(GoodsInfo.id.in_(goods_ids), GoodsInfo.unit_no!=session['unit_no']))
            total = q.count()
            return jsonify(success=False, msg=u'此订单中有非本集团商品,提交订单失败', total=total,
                           data=[{'id': g.id, 'goods_name': g.goods_name} for g in q.all()])

        # 获取订单商品的采购价
        for g in q.all():
            purchase_price[g.id] = g.purchase_price  # {'ca993ebe-3541-4d17-a66f-0eb2dd2d5635': 200, ...}

        # 检查库存是否充足
        for _gid in order_goods_counts.keys():
            _q = db_session.query(GoodsInfo).filter(GoodsInfo.id == _gid)
            if _q.one().goods_amount < order_goods_counts[_gid]:
                _goods_info = db_session.query(GoodsInfo).filter(GoodsInfo.id == _gid)
                _goods_name = '' if not _goods_info.count() else _goods_info.one().goods_name
                goods_not_enough.append(_goods_name)
        if goods_not_enough:
            db_session.rollback()
            msg = u'以下商品库存不足:</br>' + '</br>'.join(goods_not_enough)
            return jsonify(success=False, msg=msg)

        # 减库存
        for g in order:
            _q = db_session.query(GoodsInfo).filter(GoodsInfo.id == g['goods_id'])
            _q.update({'goods_amount': _q.one().goods_amount - int(g['goods_amount'])})
            profit += int(g['goods_amount']) * (float(g['price']) * 100 - purchase_price[g['goods_id']])
            goods_amount += int(g['goods_amount'])
            sale_order_details.append(
                SaleOrderDetail(id=str(uuid.uuid4()),
                                order_id=order_id,
                                goods_id=g['goods_id'],
                                goods_amount=g['goods_amount'],
                                purchase_price=purchase_price[g['goods_id']],  # 进货价
                                sale_price=float(g['price']) * 100,  # 售价
                                discount=g['discount']))  # 折扣
            payment_amount += float(g['discounted_money_amount']) * 100

            # 生成订单信息
            print payment_amount
            sale_order = SaleOrderInfo(id=order_id,
                                       create_time=datetime.datetime.now(),
                                       goods_amount=goods_amount,
                                       profit=profit,
                                       amount=payment_amount,
                                       is_paid=False,
                                       user_no=session['user_no'],
                                       unit_no=session['unit_no'])

            db_session.add(sale_order)
            db_session.flush()
            db_session.add_all(sale_order_details)
            db_session.commit()
            return jsonify(success=True, msg=u'添加订单成功',
                           data={'order_id': order_id, 'amount': payment_amount, 'goods_amount': goods_amount})


class Order(MethodView):
    @authority.permission_required('01104')
    def put(self, order_id, action):
        def process(order_id, action):
            if action == 'pay':
                i = request.json
                order_id = i.get('order_id', '').strip()
                mode = i.get('mode')
                card = i.get('card')
                cash = i.get('cash')

                # 是否是本集团的订单？
                q = db_session.query(SaleOrderInfo)
                q = q.filter(and_(SaleOrderInfo.id == order_id, SaleOrderInfo.unit_no == session['unit_no']))
                if not q.count():
                    return jsonify(success=False, msg=u'无此订单', show_msg=True)

                # 如果有订单，是否已支付？
                order = q.one()
                if order.is_paid == True:
                    return jsonify(success=False, msg=u'此单已付款(订单ID:%s)' % order_id, show_msg=True)

                # 订单金额
                order_amount = order.amount

                # 支付总额是否小于订单总额？
                print int(float(card['amount'])*100) + int(float(cash['amount'])*100)
                print order_amount
                if int(float(card['amount'])*100) + int(float(cash['amount'])*100) < order_amount:
                    return jsonify(success=False, msg=u'支付总额小于订单总额，支付失败，请重试', show_msg=True)

                # 根据付款方式的不同处理订单
                if mode in ('card', 'mixed'):  # 卡付或联合支付
                    # 是否有默认终端?
                    if not session['default_terminal']:
                        return jsonify(success=False, msg=u'无默认终端,请先设置默认终端', show_msg=True)
                    # 组装报文
                    card_pay_result = self.pay(int(float(card['amount'])*100), card['card_no'],
                                               card['track_2'], card['password'])
                    if card_pay_result['result_code'] != '0':  # 卡付款部分不成功，返回错误信息
                        return jsonify(success=False, msg=get_result_message(card_pay_result['result_code']),
                                       show_msg=True)

                    # 登记付款信息
                    order.is_paid = True
                    order.mode_of_payment = 'mixed'
                    order.cash_pay_amount = int(float(cash['amount'])*100)
                    order.card_pay_amount = int(float(card['amount'])*100)
                    order.pay_time = datetime.datetime.now()
                    db_session.add(order)
                    db_session.commit()
                    return jsonify(success=True, msg=u'付款成功')

                if mode == 'cash': # 现金支付
                    if float(cash['amount']) * 100 < order_amount:
                        return jsonify(success=False,
                                       msg=u'付款失败。此单应付%.2f元，实付%.2f元，付款失败。' % (order_amount/100.00, float(cash['amount'])),
                                       show_msg=True)

                    # 以上检测通过，付款
                    order.is_paid = True
                    order.mode_of_payment = 'cash'
                    order.cash_pay_amount = order_amount
                    db_session.add(order)
                    db_session.commit()
                    return jsonify(success=True, msg=u'付款成功')

        payment_result = process(order_id, action)
        payment_result = json.loads(payment_result.data)
        if payment_result['success']:
            S = aliased(SaleOrderDetail)
            G = aliased(GoodsInfo)
            goods = db_session.query(S.goods_amount, S.sale_price, G.goods_name) \
                              .outerjoin(G, S.goods_id == G.id) \
                              .filter(S.order_id == order_id)
            ticket = u"  **购物小票** \n"
            ticket = u'%s%s\n' % (ticket, '-' * 25)

            index = 1
            total_amount = 0
            for g in goods:
                ticket = u"%s%s. %s\n" % (ticket, index, g.goods_name)
                ticket = u"%s  数量:%s 单价:%s 金额:%s\n" % (ticket, g.goods_amount, g.sale_price/100.00, (g.goods_amount * g.sale_price)/100.00)
                index += 1
                total_amount += g.goods_amount * g.sale_price
            ticket = u"\n%s合计:￥%s\n" % (ticket, total_amount/100.00)
            ticket = u"%s%s\n" % (ticket, '-' * 25)
            ticket_info = {'content': ticket, 'length': index * 10 + 20}  # length 是打印小票的长度
            return jsonify(success=True, msg=u'付款成功', ticket=ticket_info)
        else:
            return jsonify(success=False, msg=payment_result['msg'], show_msg=True)

    @authority.permission_required('01104')
    def pay(self, amount, card_no, track_2, password):
        # 接收提交的数据
        input = request.json
        #  000010:  消费

        trans = BufferTrans()
        # 交易类型
        trans.action = '000010'
        trans.shop_no = session['shop_no']
        # 终端号
        trans.terminal_no = session['default_terminal']
        # 卡号
        trans.card_no = card_no
        # 交易金额
        trans.amount = amount
        # 二磁道
        trans.track_2 = track_2
        # 卡密码
        trans.password = password
        # 客户端版本
        trans.client_version = '1.0'
        # 交易界面，1 for B/S
        trans.interface = '1'

        print dir(trans)
        print type(trans)
        trans_string = trans.SerializeToString()
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        s.connect(('127.0.0.1', 8005))
        s.send(trans_string)
        result = s.recv(4096)
        result = eval(result)
        return result


# 收入
class Income(MethodView):
    def get(self):
        i = request.args
        today = datetime.datetime.now().strftime('%Y%m%d')
        date = i.get('date', today).strip()
        type_ = i.get('type', 'total').strip()  # 收入类型：card/cash/total

        if type_ in ('card', 'total'):
            if date == today:
                TransTable = aliased(Trans)
            else:
                TransTable = aliased(HistoryTrans)

            q_card = db_session.query(func.sum(HistoryTrans.amount).label('amount')) \
                .filter(TransTable.trans_date == date) \
                .filter(TransTable.trans_code == '000010') \
                .filter(TransTable.status == '0')

            if session['user_level'] == 'unit':
                q_card = q_card.filter(TransTable.unit_no == session['unit_no'])
            if session['user_level'] == 'shop':
                q_card = q_card.filter(TransTable.shop_no == session['shop_no'])

        if type_ in ('cash', 'total'):
            q_cash = db_session.query(func.sum(SaleOrderInfo.cash_pay_amount).label('amount')) \
                .filter(SaleOrderInfo.is_paid == True) \
                .filter(SaleOrderInfo.pay_time == '20000000')

        if type_ == 'card':
            return jsonify(success=True, total=q_card.one().amount)
        if type_ == 'cash':

            return jsonify(success=True, total=q_cash.one().amount)
        #if type_ == 'total':
        #    return jsonify(success=True,
        #                   total=q_card.one().amount + q_cash.one().amount if session['user_level'] == 'unit' else 0)


# 订单商品明细
class OrderDetail(MethodView):
    @authority.permission_required('01105')
    def get(self, order_id):
        order_id = order_id.strip()
        if not order_id:
            return jsonify(success=False, msg=u'无效的订单号', show_msg=True)

        S = aliased(SaleOrderDetail)
        G = aliased(GoodsInfo)
        q = db_session.query(S.sale_price, S.goods_amount, G.goods_name) \
                      .outerjoin(G, S.goods_id == G.id) \
                      .filter(S.order_id == order_id)
        return jsonify(success=True, total=q.count(), page=1, limit=9999,
                       data=[{'goods_name': g.goods_name,
                              'goods_amount': g.goods_amount,
                              'goods_price': g.sale_price} for g in q.all()])


# 商品销售明细
# 返回一定时期内各种商品的销售情况
class SoldGoodsReport(MethodView):
    def get(self):
        today = datetime.datetime.now().strftime("%Y%m%d")
        i = request.args
        page = int(i.get('page', 1))
        limit = int(i.get('limit', 10))

        try:
            #start_date = datetime.datetime.strptime(i.get('start_date', today).replace('/', ''), '%Y%m%d')
            # Next Line For Test ONLY!!!:
            start_date = datetime.datetime.strptime('2014601', '%Y%m%d')
            end_date = datetime.datetime.strptime(i.get('end_date', today).replace('/', ''), '%Y%m%d')
        except Exception:
            return jsonify(success=False, msg=u'日期格式不正确', show_msg=True)

        if start_date > end_date:
            return jsonify(success=False, msg=u'起始日期不能大于结束日期', show_msg=True)

        q = db_session.query(func.sum(SaleOrderDetail.goods_amount).label('goods_amount'), \
                             SaleOrderDetail.sale_price, \
                             GoodsInfo.goods_name)
        q = q.outerjoin(GoodsInfo, SaleOrderDetail.goods_id == GoodsInfo.id)
        q = q.filter(SaleOrderDetail.order_id.in_(
            db_session.query(SaleOrderInfo.id) \
                .filter(SaleOrderInfo.create_time.between(start_date, end_date)) \
                .filter(SaleOrderInfo.is_paid == True) \
                .filter(SaleOrderInfo.unit_no == session['unit_no']) ))
        q = q.group_by(SaleOrderDetail.sale_price, GoodsInfo.goods_name)

        total = q.count()
        goods = q.limit(limit).offset((page - 1) * limit).all()

        return jsonify(success=True, total=total, limit=limit, page=page,
            data=[{
                'goods_amount': g.goods_amount,
                'sale_price': g.sale_price,
                'goods_name': g.goods_name
            } for g in goods])