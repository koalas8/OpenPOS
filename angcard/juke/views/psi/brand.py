# -*- encoding=utf-8 -*-

''' 商品品牌信息的管理模块 '''

from flask import request
from flask import session
from flask.views import MethodView 
from flask.json import jsonify
from juke.modules import *


def _get_by_name(brand_name):
    brand_name = str(brand_name).strip()
    q = db_session.query(BrandInfo).filter(BrandInfo.brand_name == brand_name)
    if session['user_level'] == 'unit':
            q = q.filter(BrandInfo.unit_no) == session['unit_no']
    if session['user_level'] == 'shop':
        q = q.filter(BrandInfo.shop_no) == session['shop_no']

    return q.all()


def _get_by_id(brand_id):
    brand_id = str(brand_id).strip()
    q = db_session.query(BrandInfo).filter(BrandInfo.brand_id == brand_id)
    if session['user_level'] == 'unit':
            q = q.filter(BrandInfo.unit_no) == session['unit_no']
    if session['user_level'] == 'shop':
        q = q.filter(BrandInfo.shop_no) == session['shop_no']

    try:
        return q.one()
    except:
        return []


class Brand(MethodView):
    def post(self, brand_id):
        brand = _get_by_id(brand_id)
        if not brand:
            return jsonify(success=False, msg=u'您要修改的品牌不存在', show_msg=True)
        db_session.query(BrandInfo).filter(BrandInfo.id == brand_id).update({'id': brand_id})
        db_session.commit()
        return jsonify(success=True, msg=u'修改品牌名称成功', show_msg=True)


class BrandList(MethodView):
    def get(self):
        i = request.args
        page = int(i.get('page')) if i.get('page').isdigit() else 1     
        limit = int(i.get('limit')) if i.get('limit').isdigit else 10

        q = db_session.query(BrandInfo)
        if session['user_level'] == 'unit':
            q = q.filter(BrandInfo.unit_no) == session['unit_no']
        if session['user_level'] == 'shop':
            q = q.filter(BrandInfo.shop_no) == session['shop_no']

        total = q.count()
        brand_list = q.limit(limit).offset((page - 1) * limit).all()
        return jsonify(success=True, total=total, limit=limit, offset=offset,
                       data=[{'id': b.id, 'brand_name': b.brand_name} for b in brand_list])

    def post(self):
        i = request.json
        brand_name = i.get('brand_name', '').strip()
        if not brand_name:
            return jsonify(success=False, msg=u'请填写品牌名称', show_msg=True)
        if _get_by_name(brand_name):
            return jsonify(success=False, msg=u'此品牌已存在，请勿重复添加', show_msg=True)

        unit_no = session['unit_no']
        shop_no = session['shop_no']
        shop_no = shop_no if shop_no else ''

        brand = BrandInfo()
        brand.unit_no = unit_no
        brand.shop_no = shop_no
        brand.brand_name = brand_name
        db_session.add(brand)
        db_session.commit()

        return jsonify(success=True, msg=u'添加品牌成功')     

