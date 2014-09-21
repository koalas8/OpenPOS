# -*- coding=utf-8 -*-

from logger import create_logger
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from trans import Trans
from ccard.protocols.trans import Trans_pb2

logger = create_logger()

def prepare_data(parsed_data):
    ''' 将Google protocol buffer格式的数据转换成dict格式 '''
    fields = [
        'action', 'amount', 'batch_no', 'card_no', 'client_version', 'current_points', 
        'deposit_amount', 'deposit_count', 'interface', 'master_password', 'new_card_no', 
        'new_card_track_2', 'new_password', 'old_batch_no', 'old_trace_no', 'operator_account', 
        'operator_password', 'overdue_date', 'password', 'payment_amount', 'payment_count', 
        'points_deposit_amount', 'points_deposit_count', 'points_payment_amount', 
        'points_payment_count', 'renew_password', 'result_code', 'shop_name', 'shop_no', 
        'terminal_no', 'total_points', 'trace_no', 'track_2', 'trans_date', 'trans_time'
    ]

    data = {}

    for f in fields:
        if hasattr(parsed_data, f):
            data[f] = getattr(parsed_data, f)
    return data


class CardTrans(LineReceiver):

    def __init__(self):
        self.setRawMode()

    def connectionMade(self):
        print "server.py: status -> Connection Established"
        logger.info(u'连接已建立')

    def rawDataReceived(self, raw_data):
        logger.info(u'正在接收数据')
        print "server2.py rawData -> ", raw_data
        if raw_data:
            parsed_data = Trans_pb2.Trans()
            parsed_data.ParseFromString(raw_data)
            print "server.py: parsed_data -> ", parsed_data
            data = prepare_data(parsed_data)
            self.handle_card_trans(data)

    def handle_card_trans(self, data):
        print "server2.py data ->", data
        logger.debug(u'交易类型:' + data['action'])
        logger.debug(u'商户号:' + data['shop_no'])
        logger.debug(u'终端号:' + data['terminal_no'])
        logger.debug('card_no:' + data['card_no'])
        logger.debug('new_card_no:' + data['new_card_no'])
        trans_result = {}  # 定义交易结果变量
        trans = Trans(data)
        # if data['action'] == 'singin':  # 签到
        #     trans_result = trans.signin()
        if data['action'] == '000010':  # 消费
            trans_result = trans.payment()
        if data['action'] == '000030':  # 充值
            trans_result = trans.deposit()
        if data['action'] == '000190':  # 撤销
            trans_result = trans.cancel_trans()
        # if data['action'] == '000040':  # 充值撤销
        #     trans_result = trans.cancel_deposit()
        # if data['action'] == '000020':  # 消费撤销
        #     trans_result = trans.cancel_payment()
        # if data['action'] == 'reversal':                # 冲正
            # trans_result = trans.reversal()
        if data['action'] == '000110':                # 卡启用
            trans_result = trans.new_card()
        if data['action'] == '000090':           # 余额查询
            trans_result = trans.check_balance()
        if data['action'] == '000150':     # 改有效期
            trans_result = trans.change_overdue_date()
        if data['action'] == '000120':             # 换卡
            trans_result = trans.change_card()
        # if data['action'] == 'write_card':              # 补磁 *
        #     trans_result = trans.write_card()
        if data['action'] == '000140':         # 卡改密
            trans_result = trans.change_password()
        if data['action'] == '000050':          # 积分消费
            trans_result = trans.points_payment()
        # if data['action'] == '000060':   # 积分消费撤销
        #     trans_result = trans.cancel_points_payment()
        if data['action'] == 'check_points':            # 查询积分
            trans_result = trans.check_points()
        if data['action'] == '000070':          # 积分充值
            trans_result = trans.points_deposit()
        # if data['action'] == '000080':   # 积分充值撤销
        #     trans_result = trans.cancel_points_deposit()
        # if data['action'] == 'settlement':              # 结算
        #     trans_result = trans.settlement()
        # if data['action'] == 'bind_member':             # 绑定会员
        #     trans_result = trans.bind_member()

        logger.debug(u'交易结果:' + trans_result['result_code'])
        data = str(trans_result)        
        self.sendLine(data)


class CardTransFactory(Factory):
    def buildProtocol(self, addr):
        return CardTrans()


reactor.listenTCP(8005, CardTransFactory(), interface='127.0.0.1')
reactor.run()