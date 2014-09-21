#-*- coding=utf-8 -*-
from flask import session, request
from flask import Blueprint
from flask.json import jsonify
from flask.views import MethodView
from sqlalchemy.orm import aliased
from juke import authority
from juke.modules import *
from juke import app


class Template(MethodView):
    @authority.permission_required('01403')
    def get(self, template_id):
        i = request.args
        page, limit = int(i.get('page', 1)), int(i.get('limit', 20))
        SMT = aliased(SMSTemplate)
        q = db_session.query(SMT).filter(SMT.unit_no==session['unit_no'])
        if template_id:
            q = q.filter(SMT.id==template_id)
        total = q.count()
        templates = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, page=page, limit=limit, total=total,
            data=[{'id': t.id, 'name': t.template_name, 
                   'content': t.template_content, 'status': t.status} for t in templates])

    @authority.permission_required('01402')
    def put(self, template_id):
        i = request.json
        template_id = i.get('id', '').strip()
        template_name = i.get('name', '').strip()
        template_content = i.get('content', '').strip()
        if not template_name:
            return jsonify(success=False, msg=u'模板名称不能为空', show_msg=True)
        
        SMT = aliased(SMSTemplate)        
        q = db_session.query(SMT).filter(SMT.id==template_id).filter(SMT.unit_no==session['unit_no'])
        if not q.count:
            return jsonify(success=False, msg=u'无此权限', show_msg=True)

        template = q.one()
        template.template_name = template_name
        template.template_content = template_content
        db_session.add(template)
        db_session.commit()
        return jsonify(success=True, msg=u'修改成功', show_msg=True)
        
    @authority.permission_required('01401')
    def post(self):
        i = request.json
        template_name = i.get('name', '').strip()
        template_content = i.get('content', '').strip()
        if not template_name:
            return jsonify(success=False, msg=u'模板名称不能为空', show_msg=True)

        template = SMSTemplate(
            template_name=template_name, 
            template_level = session['user_level'],
            template_content=template_content, 
            unit_no=session['unit_no']
            )

        db_session.add(template)
        db_session.commit()
        return jsonify(success=True, msg=u'添加短信模板成功', show_msg=True)

template_view = Template.as_view('v_template')
app.add_url_rule('/sms/template', view_func=template_view, methods=['GET'], defaults={'template_id': None})
app.add_url_rule('/sms/template', view_func=template_view, methods=['POST'])
app.add_url_rule('/sms/template/<template_id>', view_func=template_view, methods=['GET', 'PUT'])


class SMS(MethodView):
    def get(self, phone_timestamp):
        i = request.args
        page, limit = int(i.get('page', '1').strip()), int(i.get('limit', '10').strip())
        q = db_session.query(SMSListInfo).order_by(SMSListInfo.send_datetime)

        if session['user_level'] == 'unit':
            q = q.filter(SMSListInfo.unit_no==session['unit_no'])
        if session['user_level'] == 'shop':
            q = q.filter(SMSListInfo.shop_no==session['shop_no'])

        if phone_timestamp:
            q = q.filter(SMSListInfo.phone_timestamp==phone_timestamp)

        total = q.count()
        sms_list = q.limit(limit).offset((page-1)*limit).all()
        return jsonify(success=True, total=total, limit=limit, offset=offset,
                       data=[{
                           'id': s.id,
                           'phone': s.phone,
                           'phone_timestamp': s.phone_timestamp,
                           'send_datetime': s.send_datetime,
                           'confirmed_datetime': s.confirmed_datetime,
                           'content': s.content,
                           'status': s.status
                       } for s in sms_list])

    def post(self):
        i = request.json
        phone = i.get('phone', [])  # 上送的数据是手机号+模板
        template = i.get('template', '').strip()

        checked_phone = [p for p in phone if len(p)==11 and p.isnumberic()]  # 通过检查的phone
        checked_phone = list(set(checked_phone))  # 去重

        if not checked_phone:
            return jsonify(success=False, msg=u'请选择具有有效手机号的会员')

        if not template:
            return jsonify(success=False, msg=u'请选择短信模板')

        ### 模板替换符

        #HuiYuanKaHao#  会员卡号
        #KaWeiHao#  卡片尾号
        #JiaoYiRiQi#    当前日期
        #JiaoYiShiJian# 当前时间
        #XingMing#  会员姓名
        #ZengSongJinE#  充值赠送金额
        #YuE#   充值后卡内余额
        #TempPoint# 变动积分
        #ShengYuJiCi#   账户剩余次数
        #JiFen# 账户积分
        #ShouJiHaoMa#   手机号码
        #ChengWei#  称谓
        #DengJi#    等级
        #JiaoYiFenDian  交易分店
        #FenDianMingCheng#  所属分店
        #LeiJiJiFen#    累计积分
        
        