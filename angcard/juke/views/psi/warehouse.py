#-*- coding=utf-8 -*-
import datetime
import uuid
from flask import session, request, Blueprint
from flask.json import jsonify
from flask.views import MethodView
from sqlalchemy import and_
from juke.modules import *
from juke import app
from juke import authority


# 仓库信息
class WarehouseList(MethodView):
    @authority.permission_required('01302')
    def get(self):
        i = request.args
        warehouse_id = i.get('warehouse_id', '').strip()
        page, limit = int(i.get('page', '1').strip()), int(i.get('limit', '10').strip())
        q = db_session.query(WarehouseInfo).filter(WarehouseInfo.unit_no==session['unit_no'])
        if warehouse_id:
            q = q.filter(WarehouseInfo.id==warehouse_id)
        total = q.count()
        warehouses = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit,
            data=[{'id': w.id, 'warehouse_name': w.warehouse_name, 'status': w.status} for w in warehouses])

    @authority.permission_required('01300')
    def post(self):
        i = request.json
        warehouse_name = i.get('warehouse_name', '').strip()
        if not warehouse_name:
            return jsonify(success=False, msg=u'仓库名称不能为空')
        warehouse = WarehouseInfo(id=str(uuid.uuid4()), warehouse_name=warehouse_name, unit_no=session['unit_no'])
        db_session.add(warehouse)
        db_session.commit()
        return jsonify(success=True, msg=u'添加仓库成功', show_msg=True)


class Warehouse(MethodView):
    @authority.permission_required('01301')
    def put(self, warehouse_id):
        i = request.json
        warehouse_name = i.get('warehouse_name').strip()
        if (not warehouse_id) or (not warehouse_name):
            return jsonify(success=False, msg=u'表单填写不完整', show_msg=True)
        q = db_session.query(WarehouseInfo).filter(and_(WarehouseInfo.id==warehouse_id, WarehouseInfo.unit_no==session['unit_no']))
        
        if not q.count():
            return jsonify(success=False, msg=u'无此仓库信息，您不能更新', show_msg=True)

        warehouse = q.one()
        warehouse.warehouse_name = warehouse_name
        db_session.add(warehouse)
        db_session.commit()
        return jsonify(success=True, msg=u'更新成功', show_msg=True)


# 入库单
class WarehouseReceiptList(MethodView):
    @authority.permission_required('01106')
    def get(self):
        i = request.args
        id = i.get('id', '').strip()
        page, limit = int(i.get('page', '1').strip()), int(i.get('limit', '10').strip())
        q = db_session.query(WarehouseReceiptInfo).filter(WarehouseReceiptInfo.unit_no == session['unit_no'])
        if id:
            q = q.filter(WarehouseReceiptInfo.id == id)
        total = q.count()
        receipts = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'id': r.id, 'goods_id': r.goods_id, 'goods_name': r.goods_name, 
                              'purchase_price': r.purchase_price, 'create_time': r.create_time, 'amount': r.amount} for r in receipts])

    @authority.permission_required('01103')
    def post(self):
        i = request.json
        goods_id = i.get('goods_id', '').strip()
        purchase_price = int(i.get('purchase_price', '0').strip())
        amount = int(i.get('amount', '0').strip())

        # 商品是否存在？
        q = db_session.query(GoodsInfo).filter(and_(GoodsInfo.unit_no==session['unit_no'], GoodsInfo.id==goods_id))
        if not q.count():
            return jsonify(success=False, msg=u'此商品不存在')

        goods = q.one()
        id = str(uuid.uuid4())
        receipt = WarehouseReceiptInfo(id=id, unit_no=session['unit_no'], goods_id=goods_id, goods_name=goods.goods_name,
                                       create_time=datetime.datetime.now(), purchase_price=purchase_price*100, amount=amount)
        goods.amount = goods.amount + amount
        db_session.add(receipt)
        db_session.add(goods)
        db_session.commit()
        return jsonify(success=True, msg=u'入库成功', show_msg=True)
