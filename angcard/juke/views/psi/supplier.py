#-*- coding=utf-8 -*-
import uuid
from flask import session, request, Blueprint
from flask.json import jsonify
from flask.views import MethodView
from sqlalchemy import or_, and_
from juke.modules import *
from juke import app
from juke import authority


class SupplierList(MethodView):
    @authority.permission_required('01202')
    def get(self):
        input = request.args
        supplier_id = input.get('supplier_id', '').strip()
        page, limit = int(input.get('page', '1').strip()), int(input.get('limit', '10').strip())
        keyword = input.get('keyword', '').strip()
        q = db_session.query(SupplierInfo).filter(SupplierInfo.unit_no == session['unit_no'])

        if supplier_id:
            q = q.filter(SupplierInfo.id == supplier_id)
        if keyword:
            keyword = '%' + keyword + '%'
            q = q.filter(or_(SupplierInfo.supplier_name.like(keyword), SupplierInfo.tel.like(keyword)))

        total = q.count()
        suppliers = q.limit(limit).offset((page - 1) * limit).all()
        return jsonify(success=True, total=total, limit=limit, page=page,
                       data=[{'id': s.id,
                              'supplier_name': s.supplier_name,
                              'tel': s.tel,
                              'contact': '',
                              'address': s.address,
                              'email': s.email} for s in suppliers])

    @authority.permission_required('01200')
    def post(self):
        input = request.json
        supplier_name = input.get('name', '').strip()
        contact = input.get('contact', '').strip()
        tel = input.get('tel', '').strip()
        email = input.get('email', '').strip()
        address = input.get('address', '').strip()

        if not supplier_name:
            return jsonify(success=False, msg=u'供应商名称不能为空')

        supplier = SupplierInfo()
        supplier.supplier_name = supplier_name
        supplier.contact = contact
        supplier.tel = tel
        supplier.email = email
        supplier.address = address
        supplier.unit_no = session['unit_no']
        db_session.add(supplier)
        db_session.commit()
        return jsonify(success=True, msg=u'添加供应商成功')


class Supplier(MethodView):
    @authority.permission_required('01201')
    def put(self, supplier_id):
        input = request.json
        id = supplier_id
        supplier_name = input.get('name', '').strip()
        tel = input.get('tel', '').strip()
        contact = input.get('contact', '').strip()
        email = input.get('email', '').strip()
        address = input.get('address', '').strip()

        if not id:
            return jsonify(success=False, msg=u'参数错误')
        q = db_session.query(SupplierInfo).filter(
            and_(SupplierInfo.id == id, SupplierInfo.unit_no == session['unit_no']))
        if not q.count():
            return jsonify(success=False, msg=u'无此供应商')
        supplier = q.first()
        supplier.supplier_name = supplier_name
        supplier.contact = contact
        supplier.tel = tel
        supplier.email = email
        supplier.address = address
        db_session.add(supplier)
        db_session.commit()
        return jsonify(success=True, msg=u'更新供应商成功')
