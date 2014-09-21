# -*- coding=utf-8 -*-
import base64
import json

from logger import create_logger
from trans import Trans, get_DES_key
from pyDes import *
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

logger = create_logger()


class CardTrans(LineReceiver):

    def __init__(self):
        print 'dataReceiving'
        self.setRawMode()
        self.data = ''

    def connectionMade(self):
        logger.info(u'连接已建立')

    def rawDataReceived(self, data):
        logger.info(u'正在接收数据')
        self.data += data
        if self.data.endswith('\n'):
            self.data = self.data[:-1]
            self.handler_card_trans(self.data)
            self.data = ''
            self.transport.loseConnection()

    def handler_card_trans(self, data):
        if data:
            # >>>>>>>>>>>>>> 解密数据
            # 接收到的数据格式为 "DES加密的数据" + 终端号
            # 解密方式为：
            # 1.将接收到的数据分为两部分：DES加密的数据和终端号
            # 2.去数据库中查询与此终端号对应的DES密钥
            # 3.使用DES密钥解密 DES加密的数据 部分
            print 'raw_data ->', data
            print 'len(raw_data) ->', len(data)
            terminal_no = data[-8:]
            data = base64.decodestring(data[:-8])
            print terminal_no

            key = get_DES_key(terminal_no)
            k = des(key, ECB, key, None, PAD_PKCS5)
            data = k.decrypt(data)  # 解密加密的数据

            # 转换数据的编码
            tmp_data = str(data).replace("'", '"')
            tmp_data = json.loads(tmp_data)
            data = {}
            for key in tmp_data.keys():
                data[key.encode('iso8859-1').lower()] = tmp_data[key].encode('iso8859-1')

            print '========= log for test ========'
            for k in data.keys():
                print k, '\t\t--->', data[k]
            print '===============================\n\n\n'

            trans_result = {}  # 定义交易结果变量
            trans = Trans(data)
            if data['action'] == 'singin':                  # 签到
                trans_result = trans.signin()
            if data['action'] == 'payment':                 # 消费
                trans_result = trans.payment()
            if data['action'] == 'deposit':                 # 充值
                trans_result = trans.deposit()
            if data['action'] == 'cancel_trans':            # 撤销
                trans_result = trans.cancel_trans()
            if data['action'] == 'cancel_deposit':          # 充值撤销
                trans_result = trans.cancel_deposit()
            if data['action'] == 'cancel_payment':          # 消费撤销
                trans_result = trans.cancel_payment()
            if data['action'] == 'reversal':                # 冲正
                trans_result = trans.reversal()
            if data['action'] == 'new_card':                # 卡启用
                trans_result = trans.new_card()
            if data['action'] == 'check_balance':           # 余额查询
                trans_result = trans.check_balance()
            if data['action'] == 'change_overdue_date':     # 改有效期
                trans_result = trans.change_overdue_date()
            if data['action'] == 'change_card':             # 换卡
                trans_result = trans.change_card()
            if data['action'] == 'write_card':              # 补磁 *
                trans_result = trans.write_card()
            if data['action'] == 'change_password':         # 卡改密
                trans_result = trans.change_password()
            if data['action'] == 'points_payment':          # 积分消费
                trans_result = trans.points_payment()
            if data['action'] == 'cancel_points_payment':   # 积分消费撤销
                trans_result = trans.cancel_points_payment()
            if data['action'] == 'check_points':            # 查询积分
                trans_result = trans.check_points()
            if data['action'] == 'points_deposit':          # 积分充值
                trans_result = trans.points_deposit()
            if data['action'] == 'cancel_points_deposit':   # 积分充值撤销
                trans_result = trans.cancel_points_deposit()
            if data['action'] == 'settlement':              # 结算
                trans_result = trans.settlement()
            if data['action'] == 'bind_member':             # 绑定会员
                trans_result = trans.bind_member()

            ###########返回信息###########
            print '========= log for test ========'
            for k in trans_result.keys():
                print k, '\t\t<---', trans_result[k]
            print '===============================\n\n\n'
            data = str(trans_result)
            print 'returned data', data
            self.sendLine(data)


class CardTransFactory(Factory):

    def buildProtocol(self, addr):
        return CardTrans()


reactor.listenTCP(8003, CardTransFactory(), interface='0.0.0.0')
reactor.run()