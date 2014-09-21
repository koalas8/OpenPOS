#-*- coding=utf-8 -*-
import uuid
from datetime import datetime
from flask import session, request
from flask.json import jsonify
from flask.views import MethodView
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import desc
from juke.modules import *
from juke import authority
from juke.utils.number import Number


# 商品基本信息
class GoodsBaseInfoList(MethodView):
    @authority.permission_required('01102')
    def get(self):
        i = request.args
        class_id = i.get('class_id', '').strip()
        goods_id = i.get('id', '').strip()
        page, limit = int(i.get('page', '1').strip()), int(i.get('limit', '10').strip())
        keyword = i.get('keyword', '').strip()
        if keyword:
            keyword = '%' + keyword + '%'

        q = db_session.query(GoodsBaseInfo).filter(GoodsBaseInfo.unit_no == session['unit_no'])
        if session['shop_no']:
            q = q.filter(GoodsBaseInfo.shop_no == session['shop_no'])
        if goods_id:
            q = q.filter(GoodsBaseInfo.id == goods_id)
        if class_id:
            q = q.filter(GoodsBaseInfo.class_id == class_id)

        if keyword:
            q = q.filter(or_(
                GoodsBaseInfo.goods_name.like(keyword),
                GoodsBaseInfo.pinyin.like(keyword),
                GoodsBaseInfo.barcode.like(keyword)
            ))
        total = q.count()
        goods = q.limit(limit).offset((page - 1) * limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'id': g.id, 'goods_name': g.goods_name} for g in goods])

    @authority.permission_required('01100')
    def post(self):
        i = request.json
        class_id = i.get('class_id', '').strip()
        goods_name = i.get('goods_name', '').strip()
        barcode = i.get('barcode', '').strip()
        supplier_id = i.get('supplier_id', '').strip()
        supplier_id = supplier_id if supplier_id else None

        # 检查商品名称和供应商名称是否正确
        if not goods_name:
            return jsonify(success=False, msg=u'商品名不正确')
        if supplier_id and not db_session.query(SupplierInfo).filter(SupplierInfo.id == supplier_id).count():
            return jsonify(success=False, msg=u'供应商不正确')

        shop_no = session['shop_no']
        shop_no = shop_no if shop_no else ''
        goods = GoodsBaseInfo(id=str(uuid.uuid4()), goods_name=goods_name, class_id=class_id,
                              barcode=barcode, supplier_id=supplier_id, unit_no=session['unit_no'],
                              shop_no=shop_no)

        db_session.add(goods)
        db_session.commit()
        return jsonify(success=True, msg=u'添加商品成功')


class MyGoodsBaseInfo(MethodView):  # 为了防止与modules.py中的GoodsBaseInfo冲突，故加前缀'My'
    def put(self):
        i = request.json
        goods_id = i.get('goods_id', '').strip()
        goods_name = i.get('goods_name', '').strip()
        barcode = i.get('barcode', '').strip()
        supplier_id = i.get('supplier_id', '').strip()

        if not goods_id:
            return jsonify(success=False, msg=u'无此商品')
        if not goods_name:
            return jsonify(success=False, msg=u'商品名称不正确')

        q = db_session.query(GoodsBaseInfo).filter(GoodsBaseInfo.id == goods_id)
        if not q.count():
            return jsonify(success=False, msu=u'无此商品')
        goods = q.one()
        goods.goods_name = goods_name
        goods.barcode = barcode
        goods.supplier_id = supplier_id
        db_session.add(goods)
        db_session.commit()
        return jsonify(success=True, msg=u'更新商品基础信息成功')

    @staticmethod
    def get_goods_name(goods_id):
        q = db_session.query(GoodsBaseInfo).filter(GoodsBaseInfo.id == goods_id)
        return q.one().goods_name if q.count() else ''


# 商品信息
class GoodsList(MethodView):
    def get(self):
        i = request.args
        id = i.get('id', '').strip()
        page = int(i.get('page', 1))
        limit = int(i.get('limit', 10))
        keyword = i.get('keyword', '').strip()
        action = i.get('action', '').strip()  # action=='sale' 时不显示库存为0的商品

        if keyword:
            keyword = '%' + keyword + '%'

        q = db_session.query(GoodsInfo).filter(GoodsInfo.unit_no == session['unit_no'])
        if session['shop_no']:
            q = q.filter(GoodsInfo.shop_no == session['shop_no'])
        if id:
            q = q.filter(GoodsInfo.id == id)
        if keyword:
            q = q.filter(GoodsInfo.goods_name.like(keyword))
        if action.lower() == 'sale':
            q = q.filter(GoodsInfo.goods_amount > 0)

        total = q.count()
        goods = q.limit(limit).offset((page - 1) * limit).all()

        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'id': g.id, 'goods_name': g.goods_name, 'color': g.color,
                              'size': g.size, 'goods_amount': g.goods_amount,
                              'purchase_price': g.purchase_price,
                              'label_price': g.label_price, 'sale_price': g.sale_price}
                             for g in goods])


class Goods(MethodView):
    @authority.permission_required('01101')
    def put(self, goods_id):
        i = request.json
        id = goods_id.strip()
        goods_name = i.get('goods_name', '').strip()
        pack_unit = i.get('pack_unit', u'件').strip()
        barcode = i.get('barcode', '').strip()
        brief_code = i.get('brief_code', '').strip()
        price = int(float(i.get('price', '0.00')) * 100)
        if not goods_name:
            return jsonify(success=False, msg=u'商品名不正确')
        db_session.query(GoodsInfo).filter(GoodsInfo.id == id) \
            .filter(GoodsInfo.unit_no == session['unit_no']) \
            .update({'goods_name': goods_name, 'pack_unit': pack_unit, 'barcode': barcode,
                     'brief_code': brief_code, 'price': price})
        db_session.commit()
        return jsonify(success=True, msg=u'更新商品信息成功')

    def get(self, goods_id):
        id = goods_id.strip()
        q = db_session.query(GoodsInfo) \
            .filter(GoodsInfo.unit_no == session['unit_no']) \
            .filter(GoodsInfo.id == id)
        if not q.count():
            return jsonify(success=False, msg=u'无此商品', show_msg=True)

        goods = q.one()
        return jsonify(success=True, data={'goods_name': goods.goods_name})


# 商品分类列表
class GoodsClassList(MethodView):
    def get(self):
        pid = request.args.get('id', '').strip()
        pid = pid if pid else None

        q = db_session.query(GoodsClassInfo).filter(GoodsClassInfo.pid == pid)
        if session['user_level'] == 'unit':
            q = q.filter(GoodsClassInfo.unit_no == session['unit_no'])
        if session['user_level'] == 'shop':
            q = q.filter(GoodsClassInfo.shop_no == session['shop_no'])
        classes = q.all()
        return jsonify(
            success=True,
            total=q.count(),
            limit=0,
            offset=0,
            data=[{
                'id': c.id,
                'pid': c.pid,
                'class_name': c.class_name
                } for c in classes])

    def post(self):
        class_name = request.json.get('class_name', '').strip()
        pid = request.json.get('pid', '').strip()
        pid = pid if pid else None

        if not class_name:
            return jsonify(success=False, msg=u'请输入正确的商品分类名称', show_msg=True)

        # q = db_session.query(GoodsClassInfo)
        # q = q.filter(GoodsClassInfo.class_name == class_name)
        # q = q.filter(GoodsClassInfo.unit_no == session['unit_no'])
        # if session['shop_no']:
        #     q = q.filter(GoodsClassInfo.shop_no == session['shop_no'])
        # if q.count():
        #     return jsonify(success=False, msg=u'此商品分类名称已经存在', show_msg=True)

        goods_class = GoodsClassInfo()
        goods_class.id = str(uuid.uuid4())
        goods_class.pid = pid
        goods_class.class_name = class_name
        goods_class.unit_no = session['unit_no']
        goods_class.shop_no = session['shop_no'] if session['shop_no'] else None
        db_session.add(goods_class)
        db_session.commit()
        return jsonify(success=True, msg=u'添加商品分类成功', show_msg=True,
                       data={'id': goods_class.id, 'pid': pid, 'class_name': class_name})


# 商品分类
class GoodsClass(MethodView):
    @staticmethod
    def get_by_id(class_id):
        user_level = session['user_level']
        unit_no = session['unit_no']
        shop_no = session['shop_no']

        q = db_session.query(GoodsClassInfo)
        q = q.filter(GoodsClassInfo.id == class_id)
        if user_level == 'unit':
            q = q.filter(GoodsClassInfo.unit_no == unit_no)
        if user_level == 'shop':
            q = q.filter(GoodsClassInfo.shop_no == shop_no)

        return q.one() if q.count() else None

    def get(self, class_id):
        goods_class = self.get_by_id(class_id)

        if not goods_class:
            return jsonify(success=False, msg=u'无此商品分类', show_msg=True)
        return jsonify(success=True,
                       data={'id': goods_class.id,
                             'class_name': goods_class.class_name})

    def put(self, class_id):
        class_name = request.json.get('class_name', '').strip()
        if not class_name:
            return jsonify(success=False, msg=u'无效的分类名称', show_msg=True)

        goods_class = self.get_by_id(class_id)
        if not goods_class:
            return jsonify(success=False, msg=u'无此商品分类', show_msg=True)

        db_session.query(GoodsClassInfo) \
                  .filter(GoodsClassInfo.id == class_id) \
                  .update({'class_name': class_name})
        db_session.commit()
        return jsonify(success=True, msg=u'修改商品分类成功', show_msg=True)

    def delete(self):
        class_id = request.json.get('class_id', '').strip()
        force_delete = request.json.get('force_delete', False)
        if not class_id:
            return jsonify(success=False, msg=u'请选择要删除的商品分类', show_msg=True)

        if self.get_by_id(class_id) is None:
            return jsonify(success=False, msg=u'无此商品分类', show_msg=True)

        # Find all sub classes which will be deleted
        classes_to_be_deleted = [class_id]
        base_goods_to_be_deleted = []
        goods_to_be_deleted = []

        sub_goods_to_be_deleted = [class_id]
        while sub_goods_to_be_deleted:
            q = db_session.query(GoodsClassInfo.id) \
                          .filter(GoodsClassInfo.pid.in_(class_id))
            sub_goods_to_be_deleted = [c.id for c in q.all()]
            if sub_goods_to_be_deleted:
                classes_to_be_deleted.extend(sub_goods_to_be_deleted)

        # Find all base good informations belongs to the classes
        # which will be deleted.
        q = db_session.query(GoodsBaseInfo.id) \
                      .filter(GoodsBaseInfo.class_id.in_(classes_to_be_deleted))
        base_goods_to_be_deleted = [g.id for g in q.all()]

        # Find all goods informations belongs to the base goods
        # informations which will be deleted.
        q = db_session.query(GoodsInfo.id) \
                      .filter(GoodsInfo.goods_id.in_(base_goods_to_be_deleted))
        goods_to_be_deleted = [g.id for g in q.all()]

        if not force_delete and goods_to_be_deleted:
            return jsonify(success=False, msg=u'此分类下还有商品信息，不能删除')

        if force_delete:
            db_session.query(GoodsClassInfo) \
                      .filter(GoodsClassInfo.id.in_(classes_to_be_deleted)) \
                      .update({'status': '1'}, False)
            db_session.query(GoodsBaseInfo) \
                      .filter(GoodsBaseInfo.id.in_(base_goods_to_be_deleted)) \
                      .update({'status': '1'}, False)
            db_session.query(GoodsInfo) \
                      .filter(GoodsInfo.id.in_(goods_to_be_deleted)) \
                      .update({'status': '1'}, False)
            db_session.commit()
            return jsonify(success=True, msg=u'此分类下的所有分类及商品已全部删除',
                           show_msg=True)


class PurchaseOrderList(MethodView):
    def _get_goods_name(self, goods_id):
        return db_session.query(GoodsBaseInfo) \
                         .filter(GoodsBaseInfo.id == goods_id.strip()) \
                         .one().goods_name

    def get(self):
        i = request.args
        limit = int(i.get('limit', 10))
        page = int(i.get('page', 1))

        GPOI = aliased(GoodsPurchaseOrderInfo)
        q = db_session.query(GPOI).filter(GPOI.unit_no == session['unit_no'])
        q = q.order_by(desc(GPOI.create_datetime))
        if session['shop_no']:
            q = q.filter(GPOI.shop_no == session['shop_no'])
        total = q.count()
        q = q.limit(limit).offset((page - 1) * limit)
        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'id': r.id,
                              'create_datetime': r.create_datetime.strftime('%Y/%m/%d %H:%M:%S'),
                              'goods_amount': r.goods_amount,
                              'cash_amount': r.cash_amount} for r in q.all()])

    def post(self):
        order = request.json.get('data', [])
        if not order:
            return jsonify(success=False, msg=u'采购单内无商品', show_msg=True)

        # order.data.item的格式：
        # {id: '',
        #  color: '',
        #  price: '',
        #  sizes: {
        #    尺码1: '值',
        #    尺码2: '值',
        #    ...,
        #    尺码n: '值'
        #  }
        # }
        order_cash_amount = 0
        order_goods_count = 0
        purchase_order_id = str(uuid.uuid4())

        purchase_order = GoodsPurchaseOrderInfo()
        purchase_order.id = purchase_order_id
        purchase_order.creator = session['user_no']
        purchase_order.create_datetime = datetime.now()
        purchase_order.unit_no = session['unit_no']
        purchase_order.shop_no = session['shop_no'] if session['shop_no'] else ''

        db_session.add(purchase_order)
        db_session.flush()

        for item in order['data']:
            # 价格是否正确？
            purchase_price = item.get('purchase_price', '0').strip()
            label_price = item.get('label_price', '0').strip()
            sale_price = item.get('sale_price', '0').strip()

            # 先将没有填写的价格转换为0
            purchase_price = purchase_price if purchase_price else '0'
            label_price = label_price if label_price else '0'
            sale_price = sale_price if sale_price else '0'
            print purchase_price
            if not (Number.is_decimal(purchase_price) or purchase_price.isdigit()):
                db_session.rollback()
                return jsonify(success=False, msg=u'%s的采购价格不正确' % self._get_goods_name(item['id']), show_msg=True)
            if not (Number.is_decimal(label_price) or label_price.isdigit()):
                db_session.rollback()
                return jsonify(success=False, msg=u'%s的吊牌价格不正确' % self._get_goods_name(item['id']), show_msg=True)
            if not(Number.is_decimal(sale_price) or sale_price.isdigit()):
                db_session.rollback()
                return jsonify(success=False, msg=u'%s的零售价格不正确' % self._get_goods_name(item['id']), show_msg=True)
            else:
                purchase_price = int(float(purchase_price) * 100)
                label_price = int(float(label_price) * 100)
                sale_price = int(float(sale_price) * 100)

            # 检查一下所填写的数量是否正确
            for key in item['sizes'].keys():
                val = str(item['sizes'][key]).strip()
                if val == '':
                    item['sizes'][key] = 0
                    continue
                if not val.isdigit():
                    db_session.rollback()

                    goods_name = self._get_goods_name(item['id'])
                    return jsonify(success=False,
                                   msg=u'商品%s %s码的采购数量不正确' % (goods_name, key),
                                   show_msg=True)

            for s in item['sizes'].keys():
                goods = GoodsInfo()
                goods.goods_id = item['id'].strip()
                goods.goods_name = MyGoodsBaseInfo.get_goods_name(item['id'].strip())
                goods.color = item['color'].strip()
                goods.purchase_price = purchase_price  # 在上面已转为以分计单位
                goods.label_price = label_price
                goods.sale_price = sale_price
                goods.size = s.strip()
                goods.goods_amount = int(item['sizes'][s])
                goods.purchase_order_id = purchase_order_id
                goods.unit_no = session['unit_no']
                goods.shop_no = session['shop_no'] if session['shop_no'] else ''
                db_session.add(goods)

                order_goods_count += goods.goods_amount
                order_cash_amount += goods.purchase_price * goods.goods_amount

            db_session.query(GoodsPurchaseOrderInfo) \
                      .filter(GoodsPurchaseOrderInfo.id == purchase_order_id) \
                      .update({'goods_amount': order_goods_count, 'cash_amount': order_cash_amount})
            db_session.flush()

        db_session.commit()
        return jsonify(success=True, msg=u'添加采购单成功', show_msg=True)