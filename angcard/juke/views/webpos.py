#-*- coding=utf-8 -*-
import socket
from flask import session, request, render_template, Blueprint
from flask.json import jsonify
from flask.views import MethodView
from juke.ccard.protocols.trans.Trans_pb2 import Trans as BufferTrans
from juke.modules import *
from juke import app


result_code_dim = {
    '0': u'交易成功',
    '2': u'商户号不存在',
    '3': u'终端号不存在',
    '4': u'卡已挂失',
    '5': u'卡已冻结',
    '6': u'卡已作废',
    '7': u'卡已过期',
    '8': u'非本系统卡',
    '9': u'非本集团卡',
    '10': u'无效卡号',
    '11': u'新卡未启用',
    '12': u'卡已启用',
    '13': u'未知错误',
    '14': u'密码错',
    '15': u'服务器错误',
    '16': u'无效金额',
    '17': u'余额不足',
    '18': u'交易记录未找到',
    '19': u'无效积分',
    '20': u'积分不足',
    '21': u'交易已撤销',
    '22': u'原交易不能撤销',
    '23': u'非法卡',
    '24': u'批次号错',
    '25': u'流水号错',
    '26': u'POS操作员不存在',
    '27': u'POS操作员密码错',
    '28': u'POS操作员已冻结',
    '29': u'账不平',
    '30': u'该卡无此功能',
    '31': u'终端无此权限',
    '32': u'无效金额格式',
    '33': u'无效日期格式',
    '61': u'该卡已经绑定'
}

trans_code_dim = {
    '000000': u'签到',
    '000010': u'消费',
    '000020': u'消费撤销',
    '000030': u'充值',
    '000040': u'充值撤销',
    '000050': u'积分消费',
    '000060': u'积分消费撤销',
    '000070': u'积分充值',
    '000080': u'积分充值撤销',
    '000090': u'余额查询',
    '000100': u'积分查询',
    '000110': u'卡启用',
    '000120': u'换卡',
    '000130': u'补磁',
    '000140': u'卡改密码',
    '000150': u'卡改有效期'
}

SOCKET_SERVER = app.config['WEBPOS_HOST']
SOCKET_PORT = app.config['WEBPOS_PORT']


def send_socket_message(msg):
    ''' 以socket方式发送数据并接收返回 '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    s.connect((SOCKET_SERVER, SOCKET_PORT))
    s.send(msg)
    data = s.recv(4096)
    return data


class DefaultTerminal(MethodView):
    def post(self):
        input = request.json()
        terminal_no = input.get('terminal_no', '').strip()
        if not terminal_no:
            return jsonify(success=False, msg=u'设置默认终端失败：无效的终端号')

        q = db_session.query(TerminalInfo) \
            .filter(TerminalInfo.terminal_no==terminal_no) \
            .filter(TerminalInfo.shop_no.in_(db_session.query(ShopInfo).filter(ShopInfo.unit_no==session['unit_no'])))

        if q.count():
            if q.one().status == '0':
                session['default_terminal'] == terminal_no
                return jsonify(success=True, msg=u'设置终端号成功', show_msg=True)
            else:
                return jsonify(success=False, msg=u'设置默认终端失败：此终端不可用', show_msg=True)
        else:
            return jsonify(success=False, msg=u'设置默认终端失败：无此终端', show_msg=True)


class WebTrans(MethodView):
    def post(self):
        # 是否有默认终端?
        if not session['default_terminal']:
            return jsonify(success=False, msg=u'无默认终端,请先设置默认终端', show_msg=True)
        # 接收提交的数据
        input = request.json
        action = input.get('trans_code', '').strip()              
        #  000010:  消费 *
        #  000020:  消费撤销 *
        #  000030:  充值 *
        #  000040:  充值撤销 *
        #  000050:  积分消费 *
        #  000060:  积分消费撤销 *
        #  000070:  积分充值 *
        #  000080:  积分充值撤销 *
        #  000090： 余额查询 *
        #  000110:  卡启用 *
        #  000140:  卡改密码 *
        #  000150:  卡改有效期 *
         
        trans = BufferTrans()
        # 交易类型
        trans.action = action
        # 商户号
        if action in ['000010', '000020', '000030', '000040', '000050',
                      '000060', '000070', '000080', '000090', '000110',
                      '000120', '000140', '000150']:
            trans.shop_no = session['shop_no']
        # 终端号
        if action in ['000010', '000020', '000030', '000040', '000050',
                      '000060', '000070', '000080', '000090', '000110',
                      '000120', '000140', '000150']:
            trans.terminal_no = session['default_terminal']
        # 卡号
        if action in ['000010', '000020', '000030', '000040', '000050',
                      '000060', '000070', '000080', '000090', '000110',
                      '000120', '000140', '000150']:
            trans.card_no = input.get('card_no', '')
        # 新卡号
        if action in ['000120']:
            trans.new_card_no = input.get('new_card_no', '')
        # 交易金额
        if action in ['000010', '000030', '000050', '000070']:
            trans.amount = int(round(float(input.get('amount', 0)) * 100))
        # 批次号
        if action in ['x']:
            trans.batch_no = '0'
        # 流水号
        if action in ['x']:
            trans.trace_no = '0'
        # 二磁道
        if action in ['000010', '000020', '000030', '000040', '000050', '000060',
                      '000070', '000080', '000090', '000110', '000120', '000140', '000150']:
            track2 = input.get('track_2', '')
            trans.track_2 = trans.track_2 if track2 else '0' * 37            
            # 如果track2是 ''，则认为是自发卡，需要从数据库中获取到真正的卡号
            if not track2:
                q = db_session.query(CardInfo).filter(CardInfo.custom_card_no==trans.card_no)
                try:
                    trans.card_no = q.one().card_no
                except Exception, e:
                    return jsonify(success=False, msg=u'无此卡号')
            
        # 新卡的二磁道（补卡交易时用）
        if action in ['000120']:
            trans.new_card_track_2 = input.get('new_track_2', '')
        # 卡密码
        if action in ['000010', '000020', '000030', '000040', '000050', '000060',
                      '000070', '000080', '000090', '000110', '000120', '000140', '000150']:
            trans.password = input.get('password', '')
        # 客户端版本
        trans.client_version = '1.0'
        # 原批次号
        if action in ['000020', '000040', '000060', '000080']:
            trans.old_batch_no = input.get('old_batch_no', '')
        # 原流水号
        if action in ['000020', '000040', '000060', '000080']:
            trans.old_trace_no = input.get('old_trace_no', '')
        # 新密码
        if action in ['000140']:
            trans.new_password = input.get('new_password', '')
        # 重复新密码
        if action in ['000140']:
            trans.renew_password = input.get('renew_password', '')
        # 主管密码
        if action in ['x']:
            trans.master_password = input.get('master_password', '')
        # 过期时间
        if action in ['000150']:
            trans.overdue_date = input.get('exp_date', '20000101')
        # 交易界面，1 for B/S
        trans.interface = '1'

        print "webpos.py: trans -> ", trans
        trans_string = trans.SerializeToString()
        print "webpos.py: serialized string -> ", trans_string
        trans_result = eval(send_socket_message(trans_string))
        
        result_code = trans_result.get('result_code', '')

        if result_code != '0':
            error = result_code_dim[result_code]
            return jsonify(success=False, msg=error, show_msg=True)
        

        ##
        # 小票变量
        shop_no = trans_result.get('shop_no', '')
        shop_name = trans_result.get('shop_name', '')
        terminal_no = trans_result.get('terminal_no', '')
        operator_no = session['user_no']
        card_no = trans_result.get('card_no', '')
        trans_date = trans_result.get('trans_date', '')
        trans_time = trans_result.get('trans_time', '')
        batch_no = trans_result.get('batch_no', '')
        trace_no = trans_result.get('trace_no', '')
        trans_name = trans_code_dim[trans_result['action']]
        amount = int(trans_result.get('amount', 0.00))
        balance = int(trans_result.get('balance', 0.00))
        current_points = trans_result.get('current_points', 0.00)
        total_points = trans_result.get('total_points', 0.00)
        ticket_result = trans_result.get('result_code', '')

        ##
        # 小票文本           
        ticket = render_template('webpos/ticket.tpl',
                                 shop_name=shop_name,
                                 shop_no=shop_no,
                                 terminal_no=terminal_no,
                                 operator_no=operator_no,
                                 card_no=card_no,
                                 trans_date=trans_date,
                                 trans_time=trans_time,
                                 batch_no=batch_no,
                                 trace_no=trace_no,
                                 trans_name=trans_name,
                                 amount=float(amount) / 100.00,
                                 balance=balance,
                                 current_points=current_points,
                                 total_points=total_points)

        return jsonify(success=True, data={'ticket': ticket})

