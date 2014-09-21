#encoding=utf-8

import uuid
import time
import datetime
import hashlib

from codedim import INTERFACE
from codedim import *
from db import DB


def get_DES_key(terminal_no):
    db = DB()
    key = db.fetch_one("SELECT des_key FROM terminal_info WHERE terminal_no = %s;", (terminal_no,))
    return key['des_key']

def get_current_date():  # 获取当前日期, 格式: yyyymmdd
    return time.strftime('%Y%m%d',time.localtime(time.time()))

def get_current_time():  # 获取当前时间, 格式: hhmmss
    return time.strftime('%H%M%S',time.localtime(time.time()))


class Trans:
    def __init__(self, data):
        self.db = DB()
        self.data = data
        if not 'interface' in self.data.keys():
            self.data['interface'] = INTERFACE['desktop_soft']  #  默认的交易客户端为 C/S客户端
        if not self.data['interface'] not in INTERFACE.keys():
            self.data['interface'] == INTERFACE['desktop_soft']

        if self.data['interface'] == INTERFACE['web']:  # 如果是WEB交易,则批次号和流水号直接从数据库中取
            self.data['batch_no'] = self._get_batch_no(self.data['terminal_no'])
            self.data['trace_no'] = self._get_trace_no(self.data['terminal_no'])

        self.card_info = self._get_card_info(self.data['card_no'], self.data['shop_no'])

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 定义返回的数据
        self.rtnData = {}  # 返回的数据
        self.rtnData['action'] = self.data['action']  # 交易类型
        self.rtnData['card_no'] = self.data['card_no']  # 卡号 
        self.rtnData['shop_no'] = self.data['shop_no']  # 商户号
        self.rtnData['shop_name'] = self._get_shop_name(self.data['shop_no']).decode('utf-8')  # 商户名        
        self.rtnData['terminal_no'] = self.data['terminal_no']  # 终端号
        self.rtnData['trans_date'] = get_current_date()  # 交易日期
        self.rtnData['trans_time'] = get_current_time()  # 交易时间
        self.rtnData['trans_code'] = trans_code_dim['unknown']  # 交易码
        self.rtnData['current_points'] = 0.00  # 本次积分
        self.rtnData['total_points'] = 0.00  # 可用积分
        self.rtnData['points_rule'] = 0.00  # 积分规则
        self.rtnData['balance'] = 0  # 余额
        self.rtnData['result_code'] = "0"  # 返回码
        self.rtnData['card_type'] = self.card_info['card_type']
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 定义返回的数据         
  
    # >>>>>>辅助函数
    def _add_cash_back_task(self, trans_id, card_no, cash=0, points=0, interval=0,
                            times=0, start_date=datetime.datetime.today()):
        '''
        添加返现cron
        @param trans_id: 充值交易的id
        @param card_no: 交易卡号
        @param cash: 返多少金额
        @param points: 返多少积分
        @param interval: 间隔天数
        @param times: 返现次数
        @param start_date: 开始日期
        @return: True/False
        '''
        try:
            for i in range(0, times):
                new_date = start_date + datetime.timedelta(days=interval*(i+1))
                self.db.insert('card_deposit_task', id=str(uuid.uuid4()), trans_id=trans_id,
                               card_no=card_no, date_time=new_date, amount=cash,
                               points=points, status='1')
            return True
        except Exception, e:
            print e.message
            return False

    # 根据商户号获取商户名
    def _get_shop_name(self, shop_no):
        sql = "SELECT shop_name FROM shop_info WHERE shop_no = %s;"
        shop_info = self.db.fetch_one(sql, (shop_no,))
        return shop_info['shop_name'] if shop_info else ''

    # 获取积分规则。如果没有设置积分规则，则返回0
    def _get_points_rule(self, card_no, shop_no):
        sql_credit_unit = "SELECT unit_no FROM card_info WHERE card_no = %s;"
        sql_debit_unit = "SELECT unit_no FROM shop_info WHERE shop_no = %s;"
        credit_unit = self.db.fetch_one(sql_credit_unit, (card_no,))['unit_no']
        debit_unit = self.db.fetch_one(sql_debit_unit, (shop_no,))['unit_no']
        if credit_unit == debit_unit:  # 同一集团发的卡
            sql = "SELECT points_rule FROM shop_info WHERE shop_no = %s;"
            para = (shop_no,)
        else:
            sql = "SELECT points_rule FROM points_rule WHERE credit_unit = %s AND debit_unit = %s;"
            para = (credit_unit, debit_unit)
        points_rule = self.db.fetch_one(sql, para)
        return points_rule['points_rule'] if points_rule else 0
    
    # 获取等级的充值规则
    def _get_card_deposit_rule(self, card_no):
        sql = "SELECT * FROM member_deposit_rule WHERE id = (" \
              "    SELECT card_level_id FROM card_info WHERE card_no = %s ) ORDER BY deposit_amount DESC;"
        rules = self.db.fetch_all(sql, (card_no,))
        return rules

    # 获取批次号
    def _get_batch_no(self, terminal_no):
        return self.db.fetch_one("SELECT batch_no FROM terminal_info WHERE terminal_no = %s;", (terminal_no,))['batch_no']

    # 获取流水号
    def _get_trace_no(self, terminal_no):
        return self.db.fetch_one("SELECT trace_no FROM terminal_info WHERE terminal_no = %s;", (terminal_no,))['trace_no']

    # 设置流水号, 值为 trace_no
    def _set_trace_no(self, terminal_no, trace_no):
        return self.db.execute("UPDATE terminal_info SET trace_no = %s WHERE terminal_no = %s;", (trace_no, terminal_no))

    # 增加批次号,增量为 1
    def _increase_batch_no(self, terminal_no):
        return self.db.execute("UPDATE terminal_info SET batch_no = batch_no + 1 WHERE terminal_no = %s;", (terminal_no,))

    # 增加流水号,增量为 1
    def _increase_trace_no(self, terminal_no):
        return self.db.execute("UPDATE terminal_info SET trace_no = trace_no + 1 WHERE terminal_no = %s;", (terminal_no,))

    # 根据卡号获取卡信息。如果没有获取到，则返回None
    # 卡号可以是系统卡卡号，也可以是自发卡卡号
    def _get_card_info(self, card_no, shop_no):
        sql = """SELECT * FROM card_info WHERE card_no = %s AND unit_no = (
            SELECT unit_no FROM shop_info WHERE shop_no = %s);
        """
        card_info = self.db.fetch_one(sql, (card_no, shop_no))
        return card_info if card_info else None

    # 根据商户号和卡号来判断是否是本集团卡
    def _is_my_unit_card(self, shop_no, card_no):
        sql = """
            SELECT COUNT(*) count FROM card_info WHERE card_no = %s AND unit_no = (
                SELECT unit_no FROM shop_info WHERE shop_no = %s
                );
        """
        params = (card_no, shop_no)
        return False if self.db.fetch_one(sql, params)['count'] == 0 else True 

    # 检查批次号和流水号
    def _batch_no_trace_no_check(self, client_batch_no, client_trace_no, terminal_no):
        # 防止上送的批次号/流水号为空时产生异常
        if str(client_batch_no).strip() == '':
            client_batch_no = 0
        if str(client_trace_no).strip() == '':
            client_trace_no = 0

        # 上送的批次号要与系统的批次号相同
        sys_batch_no = int(self._get_batch_no(terminal_no))
        client_batch_no = int(client_batch_no)
        if not (client_batch_no == sys_batch_no):
            self.rtnData['result_code'] = return_code_dim['invalid_batch_no']
            return False

        # 上送的流水号要大于等于系统的流水号
        sys_trace_no = int(self._get_trace_no(terminal_no))
        client_trace_no = int(client_trace_no)
        if client_trace_no < sys_trace_no:
            self.rtnData['result_code'] = return_code_dim['invalid_trace_no']
            return False
        elif client_trace_no > sys_trace_no:
            self.db.execute("UPDATE terminal_info SET trace_no = %s WHERE terminal_no = %s;", (client_trace_no, terminal_no))
        return True

    # 判断商户和终端是否存在
    def _is_shop_terminal_valid(self, shop_no, terminal_no):
        trans_code = self.rtnData['trans_code']
        # 商户号是否存在并且可用？
        if not self.db.fetch_one("SELECT * FROM shop_info WHERE shop_no = %s AND status='0';", (shop_no,)):
            self.rtnData['result_code'] = return_code_dim['shop_not_exist']
            return False
        else:
            # 终端号是否存在并且可用？
            if not self.db.fetch_one("SELECT * FROM terminal_info WHERE shop_no = %s AND terminal_no = %s AND status = '0';", (shop_no, terminal_no)):
                self.rtnData['result_code'] = return_code_dim['terminal_not_exist']
                return False
            else:
                # 商户号终端号都存在并且可用了，那么所属集团的集团号是否可用？
                unit = self.db.fetch_one("SELECT status FROM unit_info WHERE unit_no = (SELECT unit_no FROM shop_info WHERE shop_no = %s);", (shop_no,))
                if not unit or unit['status'] == '1':
                    self.rtnData['result_code'] == return_code_dim['terminal_not_exist']
                    return False
                    
                # 终端是否有此交易权限？
                count = self.db.fetch_one("SELECT COUNT(*) count FROM terminal_trans WHERE terminal_no = %s AND trans_code = %s;", (terminal_no, trans_code))['count']
                if count > 0:
                    return True
                else:
                    self.rtnData['result_code'] = return_code_dim['forbidden_terminal_trans']
                    return False

    # 判断是否有互通关系
    def _is_interflow_relation(self, credit_card_no, debit_shop_no):
        count = self.db.fetch_one("""
                SELECT COUNT(*) count
                FROM inter_info
                WHERE credit_unit = (SELECT unit_no FROM card_info WHERE card_no = %s)
                    AND debit_unit = (SELECT unit_no FROM shop_info WHERE shop_no = %s);
            """, (credit_card_no, debit_shop_no))['count']
        if count > 0:
            return True
        else:
            self.rtnData['result_code'] = return_code_dim['outward_card']
            return False

    # 判断交易金额是否合理及正确
    def _is_amount_format(self, amount):
        amount = str(amount).strip()
        if not amount.isdigit():
            self.rtnData['result_code'] = return_code_dim['invalid_amount_format']
            return False
        if len(amount) > 10:
            self.rtnData['result_code'] = return_code_dim['invalid_amount_format']
            return False
        return True


    # 判断日期格式是否正确
    def _is_date_format(self, date):
        date = str(date).strip()
        return True
    
    # <<<<<<辅助函数



    # >>>>>>具体交易
    def _card_check(self, check_track=True, check_password=True, 
        check_status=True, check_new_card=True, check_exp_date=True):
        # 以下状态判断的顺序不能变化
        # 检查卡是否存在
        if not self.card_info:
            self.rtnData['result_code'] = return_code_dim['invalid_card_no']
            return False
        # 检查磁条
        if check_track:        
            if self.data['track_2'].strip() != self.card_info['track_2'].strip():
                self.rtnData['result_code'] = return_code_dim['illegal_card']
                return False
        # 检查密码
        if check_password:
            if str(self.card_info['password']).strip() != hashlib.md5(str(self.data['password']).strip()).hexdigest():
                self.rtnData['result_code'] = return_code_dim['wrong_password']
                return False        
        # 检查卡状态: 是否是－－挂失卡？冻结卡？无效卡？过期卡？
        if check_status:
            if self.card_info['status'] == '2':
                self.rtnData['result_code'] = return_code_dim['lost_card']
                return False
            if self.card_info['status'] == '3':
                self.rtnData['result_code'] = return_code_dim['disabled_card']
                return False
            if self.card_info['status'] == '4':
                self.rtnData['result_code'] = return_code_dim['invalid_card_no']
                return False
            if self.card_info['status'] == '6':
                self.rtnData['result_code'] = return_code_dim['invalid_card']
                return False
        # 检查卡状态: 是否是－－新发卡？
        if check_new_card:
            if self.card_info['status'] == '0':
                self.rtnData['result_code'] = return_code_dim['new_card']
                return False                
        if check_exp_date:
            print self.card_info['exp_date']  
            print get_current_date()
            if int(self.card_info['exp_date']) < int(get_current_date()):
                self.rtnData['result_code'] = return_code_dim['overdue_card']
                return False
        return True

    def _add_trans(self,trans_id=None, reversiable='0', points_rule=0, amount_balance=0,
                   points=0, points_balance=0, amount=0, award_amount=0, award_points=0, commit_db=True):
        trans_id = trans_id or str(uuid.uuid4())
        trans_id = str(trans_id)
        reversiable = str(reversiable)
        if reversiable not in ("0", "1", "2"):  # 0-交易可撤销 1-交易已撤销 2-交易不能撤销
            raise

        trans_table = "trans_%s" % datetime.datetime.now().strftime('%Y%m')
        sql = "INSERT INTO "  + trans_table + """ (
                card_no, shop_no, terminal_no,
                trans_code, trans_date, trans_time,
                result_code, reversiable, points_rule,
                points, points_balance, amount, award_amount, amount_balance,
                award_points, batch_no, trace_no,
                id, 
                credit_unit, 
                debit_unit, 
                interface
            )VALUES (
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s,
                (SELECT unit_no FROM shop_info WHERE shop_no = %s),
                %s
            );
        """
        self.rtnData['batch_no'] = self._get_batch_no(self.data['terminal_no'])
        self.rtnData['trace_no'] = self._get_trace_no(self.data['terminal_no'])        
        params = (
                self.data['card_no'], self.data['shop_no'], self.data['terminal_no'], 
                self.rtnData['trans_code'], self.rtnData['trans_date'], self.rtnData['trans_time'], 
                self.rtnData['result_code'], reversiable, points_rule, 
                points, points_balance, amount, award_amount, amount_balance,
                award_points, self.rtnData['batch_no'], self.rtnData['trace_no'],
                trans_id, self.card_info['unit_no'],
                self.data['shop_no'], self.data['interface']
            )
        self.db.execute(sql, params)
        if self.rtnData['trans_code'] in ('000010', '000020', '000030', 
                                          '000040', '000050', '000060', 
                                          '000070', '000080', '000190') \
            and self.rtnData['result_code'] == return_code_dim['success']:
            timestamp = datetime.datetime.strptime('%s%s' % (self.rtnData['trans_date'], self.rtnData['trans_time']), '%Y%m%d%H%M%S')
            self.db.execute('UPDATE card_info SET last_trans_time=%s WHERE card_no=%s;', (timestamp, self.rtnData['card_no']))
            self.db.execute('UPDATE member SET last_trans_time=%s WHERE id=(SELECT member_id FROM card_info WHERE card_no=%s);', (timestamp, self.rtnData['card_no']))
        self._increase_trace_no(self.data['terminal_no'])
        if commit_db:
            self.db.commit()
        
    def signin(self):
        #
        # 签到, 不记流水
        #
        self.rtnData['trans_code'] = trans_code_dim['singin']
        try:
            # 检查商户号与终端号
            if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
                return self.rtnData
            # 检查操作员是否存在
            operator_info = self.db.fetch_one("SELECT * FROM pos_operator WHERE operator_no = %s AND shop_no = %s;", (self.data['operator_account'], self.data['shop_no']))            
            if not operator_info:
                self.rtnData['result_code'] = return_code_dim['operator_not_exist']
                return self.rtnData
            # 检查POS操作员密码是否正确
            if not (operator_info['password'] == self.data['operator_password']):
                self.rtnData['result_code'] = return_code_dim['wrong_operator_pwd']
                return self.rtnData

            # 检查POS操作员是否已冻结
            if not operator_info['state'] == '0':
                self.rtnData['result_code'] = return_code_dim['frozen_operator']
                return self.rtnData
            # 以上检查全部通过，更新terminal_info表的操作员信息
            self.db.execute("update terminal_info SET current_pos_operator = %s WHERE terminal_no = %s;", (self.data['operator_account'], self.data['terminal_no']))
            self.rtnData['result_code'] = return_code_dim['success']
            self.rtnData['batch_no'] = self._get_batch_no(self.data['terminal_no'])
            self.rtnData['trace_no'] = self._get_trace_no(self.data['terminal_no'])
            self.db.commit()
            return self.rtnData
        except Exception, e:
            self.db.rollback()
            print "ERROR -> ", e.message
            self.rtnData['result_code'] = return_code_dim['unknown_error']
            return self.rtnData


    def payment(self):
        #
        # 消费，记流水
        #
        self.rtnData['trans_code'] = trans_code_dim['payment']
        # 检查金额格式
        if not self._is_amount_format(self.data['amount']):
            return self.rtnData
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            # 是否有互通关系
            if not self._is_interflow_relation(self.data['card_no'], self.data['shop_no']):
                self.rtnData['result_code'] = return_code_dim['outward_card']
                self._add_trans(reversiable='2')
                return self.rtnData
        # 检查卡是否有效
        if not self._card_check():
            self._add_trans(reversiable='2')
            return self.rtnData

        amount = int(str(self.data['amount']))  # 系统中交易单位为"分"
        if amount <= 0:  # 交易金额是否合法
            self.rtnData['result_code'] = return_code_dim['invalid_balance']
            self._add_trans(reversiable='2')
            return self.rtnData

        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):  # 不是本集团卡
            if not self._is_interflow_relation(self.data['card_no'], self.data['shop_no']):  # 如果无互通关系
                self.rtnData['result_code'] = return_code_dim['outward_card']
                self._add_trans(reversiable='2')
                return self.rtnData

        #开始消费交易
        try:
            points_rule = self._get_points_rule(self.data['card_no'], self.data['shop_no'])
            points = "%.0f" % (points_rule * amount / 100)  # 计算本次积分。因为金额单位为分,而计算规则为"1元:n分",所以计算出的积分要除以100        
            if int(self.card_info['amount']) < amount:  # 检查卡内金额是否足够
                self.rtnData['result_code'] = return_code_dim['balance_not_enough']
                self._add_trans(reversiable='2', amount=amount)
                return self.rtnData
            #更新此卡的余额、积分和总消费额
            self.db.execute("UPDATE card_info SET amount=(amount-%s), points = (points+%s), total_pay = (total_pay + %s) WHERE card_no=%s;", (amount, float(points), amount, self.data['card_no']))       
            #返回交易信息
            self.rtnData['amount'] = amount
            self.rtnData['points_rule'] = points_rule  # 添加交易流水(add_trans)时会用到
            self.rtnData['balance'] = int(self.card_info['amount']) - int(amount)
            self.rtnData['current_points'] = points
            self.rtnData['total_points'] = int(self.card_info['points']) + int(points)            
            self.rtnData['result_code'] = return_code_dim['success']            
            self._add_trans(reversiable='0', points_rule=points_rule, points=points, amount=amount)
            return self.rtnData
        except Exception, e:
            self.db.rollback()
            print "ERROR -> ", e.message
            self.rtnData['result_code'] = return_code_dim['unknown_error']
            return self.rtnData

    def deposit(self):
        #
        #充值
        #
        self.rtnData['trans_code'] = trans_code_dim['deposit']
        # 检查金额格式
        if not self._is_amount_format(self.data['amount']):
            return self.rtnData
        # 检查金额格式
        if not self._is_amount_format(self.data['amount']):
            return self.rtnData
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查卡是否有效
        if not self._card_check():
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查是否是充值卡  -- 2013.01.22
        if not self.card_info['property_deposit']:
            self.rtnData['result_code'] = return_code_dim['forbidden_card_feature']
            self._add_trans(reversiable="2")
            return self.rtnData
        # 获取卡的充值规则
        # rules = self._get_card_deposit_rule(self.data['card_no'])
        try:
            award_amount = 0  # 充值奖励金额
            award_points = 0  # 充值奖励积分
            interval = 0  # 返现间隔天数
            cash_back = 0  # 返现金额
            points_back = 0  # 返现积分
            times = 0  # 返现次数
            # for r in rules:
            #     # 规则要从最大值向最小值找
            #     if int(self.data['amount']) > int(r['deposit_amount']):
            #         award_amount = int(r['award_amount'])
            #         award_points = int(r['award_points'])
            #         interval = int(r['interval'])
            #         cash_back = int(r['cash_back_amount'])
            #         points_back = int(r['points_back_amount'])
            #         times = int(r['back_times'])
            #         break
            trans_id = str(uuid.uuid4())
            # 添加返现corn
            self._add_cash_back_task(trans_id=trans_id, card_no=self.data['card_no'],
                                     cash=cash_back, points=points_back,
                                     interval=interval, times=times)
            self.db.execute('UPDATE card_info SET amount = (amount + %s + %s), points = (points + %s) WHERE card_no = %s;',
                            (self.data['amount'], award_amount, award_points, self.data['card_no']))
            self.rtnData['amount'] = int(self.data['amount']) + award_amount
            self.rtnData['total_points'] = int(self.card_info['points']) + award_points
            self.rtnData['balance'] = int(self.card_info['amount']) + int(self.data['amount']) + award_amount
            self.rtnData['result_code'] = return_code_dim['success']
            self._add_trans(trans_id=trans_id, reversiable='0', amount=self.data['amount'], award_amount=award_amount, award_points=award_points)
            return self.rtnData
        except Exception, e:
            self.db.rollback()
            self.rtnData['result_code'] = return_code_dim['unknown_error']
            print "ERROR -> ", e.message
            return self.rtnData

    def new_card(self):
        #
        # 卡启用, 记流水
        #
        self.rtnData['trans_code'] = trans_code_dim['new_card']
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查卡是否已启用
        if self._card_check(check_exp_date=False):
            self.rtnData['result_code'] = return_code_dim['enabled_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        else:
            if self.rtnData['result_code'] == return_code_dim['new_card']:
                # 开始启用
                try:
                    # 计算卡的有效期
                    card_life_by_month = str(self.db.fetch_one("SELECT valid_life FROM card_info WHERE card_no = %s;", (self.data['card_no'],))['valid_life']).strip()
                    today = get_current_date()
                    card_life_by_days = int(card_life_by_month) * 30
                    card_life_by_days = datetime.timedelta(days=card_life_by_days)
                    exp_date = datetime.date(int(today[0:4]), int(today[4:6]), int(today[6:8])) + card_life_by_days
                    exp_date = exp_date.strftime('%Y%m%d')
                    # 更新卡的状态为已启用, 有效期为计算出的有效期
                    self.db.execute("UPDATE card_info SET status='1', exp_date=%s WHERE card_no = %s;", (exp_date, self.data['card_no'],))
                    # 获取新卡的信息，以便返回数据
                    card_info = self._get_card_info(self.data['card_no'], self.data['shop_no'])

                    self.rtnData['result_code'] = return_code_dim['success']
                    self.rtnData['balance'] = str(card_info['amount']).strip()
                    self.rtnData['current_points'] = "0.00"
                    self.rtnData['total_points'] = str(card_info['points']).strip()
                    self._add_trans(reversiable='0')
                    return self.rtnData
                except Exception, e:
                    self.db.rollback()
                    self.rtnData['result_code'] = return_code_dim['unknown_error']
                    print "ERROR -> ", e.message
                    return self.rtnData
            else:
                return self.rtnData

    def check_balance(self):
        #
        # 查询余额
        #
        self.rtnData['trans_code'] = trans_code_dim['check_balance']
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查卡是否有效
        if not self._card_check():
            self._add_trans(reversiable='2')
            return self.rtnData
        
        else:
            self.rtnData['result_code'] = return_code_dim['success']
            self.rtnData['total_points'] = self.card_info['points']
            self.rtnData['balance'] = str(self.card_info['amount'])
            self._add_trans(reversiable='2')
            return self.rtnData

    def change_exp_date(self):
        #
        # 修改有效期
        #
        self.rtnData['trans_code'] = trans_code_dim['change_exp_date']
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查卡是否合法
        if not self._card_check(check_status=False):
            self._add_trans(reversiable='2')
            return self.rtnData
        else:  # 下面的这部分卡状态检查是在原_card_check方法中的卡状态检查部分的基础上去除了卡有效期的检查
            if self.card_info['status'] == '2':
                self.rtnData['result_code'] = return_code_dim['lost_card']
                return self.rtnData
            if self.card_info['status'] == '3':
                self.rtnData['result_code'] = return_code_dim['disabled_card']
                return self.rtnData
            if self.card_info['status'] == '4':
                self.rtnData['result_code'] = return_code_dim['invalid_card_no']
                return self.rtnData           
        try:
            self.db.execute("UPDATE card_info SET exp_date = %s WHERE card_no = %s;", (self.data['exp_date'], self.data['card_no']))            
            self.rtnData['result_code'] = return_code_dim['success']
            self.rtnData['balance'] = self.card_info['amount']
            self.rtnData['total_points'] = self.card_info['points']
            self._add_trans(reversiable='2')
            return self.rtnData
        except Exception, e:
            self.db.rollback()        
            self.rtnData['result_code'] = return_code_dim['unknown_error']
            print "ERROR -> ", e.message
            return self.rtnData

    def change_card(self):
        #
        # 换卡
        #
        self.rtnData['trans_code'] = trans_code_dim['change_card']
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是旧卡否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查新卡是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['new_card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查旧卡是否合法
        if not self._card_check():
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查新卡是否合法
        new_card_info = self._get_card_info(self.data['new_card_no'], self.data['shop_no'])
        if not new_card_info: # 卡是否存在？
            self.rtnData['result_code'] = return_code_dim['invalid_card_no']
            self._add_trans(reversiable='2')
            return self.rtnData        
        # 检查新卡状态: 是否是－－挂失卡？冻结卡？无效卡？新发卡？过期卡？
        if new_card_info['status'] == '2':
            self.rtnData['result_code'] = return_code_dim['lost_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        if new_card_info['status'] == '3':
            self.rtnData['result_code'] = return_code_dim['disabled_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        if new_card_info['status'] == '4':
            self.rtnData['result_code'] = return_code_dim['invalid_card_no']
            self._add_trans(reversiable='2')
            return self.rtnData
        if new_card_info['status'] == '1':
            self.rtnData['result_code'] = return_code_dim['enabled_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        try:
            self.db.execute("UPDATE card_info SET status='6', amount=0, points=0, points_rule=0 WHERE card_no = %s;", (self.data['card_no'],))  # 作废旧卡
            self.db.execute("""UPDATE card_info SET status='1', amount=%s, points=%s, points_rule=%s, valid_life=%s, exp_date=%s 
                               WHERE card_no = %s;""", (self.card_info['amount'], 
                                                        self.card_info['points'], 
                                                        self.card_info['points_rule'],
                                                        self.card_info['valid_life'],
                                                        self.card_info['exp_date'],
                                                        self.data['new_card_no']))  # 启用新卡
            self.rtnData['result_code'] = return_code_dim['success']
            self._add_trans(reversiable='2')        
            return self.rtnData
        except Exception, e:
            self.db.rollback()
            self.rtnData['result_code'] = return_code_dim['unknown_error']
            print "ERROR -> ", e.message
            return self.rtnData

    def change_password(self):
        #
        # 卡改密
        #
        self.rtnData['trans_code'] = trans_code_dim['change_password']
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData            
        # 检查卡是否有效
        if not self._card_check():
            self._add_trans(reversiable='2')
            return self.rtnData
        else:
            try:
                self.db.execute("UPDATE card_info SET password = %s WHERE card_no = %s;", (hashlib.md5(self.data['new_password']).hexdigest(), self.data['card_no']))                
                self.rtnData['balance'] = self.card_info['amount']
                self.rtnData['total_points'] = self.card_info['points']
                self.rtnData['result_code'] = return_code_dim['success']
                self._add_trans(reversiable='2')
                return self.rtnData
            except Exception, e:
                self.db.rollback()
                self.rtnData['result_code'] = return_code_dim['unknown_error']
                print "ERROR -> ", e.message
                return self.rtnData

    def points_payment(self):
        #
        # 积分消费
        #
        self.rtnData['trans_code'] = trans_code_dim['points_payment']
        # 检查金额格式
        if not self._is_amount_format(self.data['amount']):
            return self.rtnData
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查卡是否有效
        if not self._card_check():
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查上送积分是否合法
        if int(str(self.data['amount'])) <= 0:
            self.rtnData['result_code'] = return_code_dim['invalid_points']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查卡内积分是否足够完成本次交易
        if str(self.data['amount']).strip() > str(self.card_info['points']).strip():
            self.rtnData['result_code'] = return_code_dim['points_not_enough']
            self._add_trans(reversiable='2')
            return self.rtnData
        try:
            self.db.execute("UPDATE card_info SET points = (points-%s) WHERE card_no = %s;", (self.data['amount'], self.data['card_no']))
            self.rtnData['total_points'] = str(int(self.card_info['points']) - int(self.data['amount']))
            self.rtnData['balance'] = self.card_info['amount']
            self.rtnData['current_points'] = - int(self.data['amount'])
            self.rtnData['result_code'] = return_code_dim['success']
            self._add_trans(reversiable='0', points_rule=0, amount=int(self.data['amount']))
            return self.rtnData
        except Exception, e:
            self.db.rollback()
            self.rtnData['result_code'] = return_code_dim['unknown_error']
            print "ERROR -> ", e.message
            return self.rtnData

    def check_points(self):
        #
        # 积分查询
        #
        self.rtnData['trans_code'] = trans_code_dim['check_points']
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            return self.rtnData
        # 检查卡是否有效
        if not self._card_check():
            return self.rtnData
        self.rtnData['amount'] = self.card_info['points']
        self.rtnData['result_code'] = return_code_dim['success']
        return self.rtnData

    def points_deposit(self):
        #
        # 积分充值
        #
        self.rtnData['trans_code'] = trans_code_dim['points_deposit']
        # 检查金额格式
        if not self._is_amount_format(self.data['amount']):
            return self.rtnData
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查上送的积分是否合法
        if int(str(self.data['amount'])) == 0:
            self.rtnData['result_code'] = return_code_dim['invalid_points']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查卡是否有效
        if not self._card_check():
            self._add_trans(reversiable='2')
            return self.rtnData
        try:
            sql = "UPDATE card_info SET points = (points + %s) WHERE card_no = %s;"
            params = (self.data['amount'], self.data['card_no'])
            self.db.execute(sql, params)
            self.rtnData['balance'] = self.card_info['amount']
            self.rtnData['current_points'] = self.data['amount']
            self.rtnData['total_points'] = int(self.card_info['points']) + int(self.data['amount'])
            self.rtnData['result_code'] = return_code_dim['success']
            self._add_trans(reversiable='0', amount=int(self.data['amount']))
            return self.rtnData
        except Exception, e:
            self.db.rollback()
            self.rtnData['result_code'] = return_code_dim['unknown_error']
            print "ERROR -> ", e.message
            return self.rtnData

    def settlement(self):
        #
        # 结算
        #
        self.rtnData['trans_code'] = trans_code_dim['settlement']
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData

        try:
            payment_count = self.db.fetch_one("""
                    SELECT COUNT(*) count 
                    FROM trans 
                    WHERE trans_code = %s AND terminal_no = %s AND result_code = %s AND reversiable = '0' AND settle_flag = false;
                """, (trans_code_dim['payment'], self.data['terminal_no'], return_code_dim['success']))['count']      
            payment_amount = self.db.fetch_one("""
                    SELECT SUM(amount) amount 
                    FROM trans 
                    WHERE trans_code = %s AND terminal_no = %s AND result_code = %s AND reversiable = '0' AND settle_flag = false;
                """, (trans_code_dim['payment'], self.data['terminal_no'], return_code_dim['success']))['amount']
            deposit_count = self.db.fetch_one("""
                    SELECT COUNT(*) count
                    FROM trans 
                    WHERE trans_code = %s AND terminal_no = %s AND result_code = %s AND reversiable = '0' AND settle_flag = false;
                """, (trans_code_dim['deposit'], self.data['terminal_no'], return_code_dim['success']))['count']
            deposit_amount = self.db.fetch_one("""
                    SELECT SUM(amount) amount 
                    FROM trans 
                    WHERE trans_code = %s AND terminal_no = %s AND result_code = %s AND reversiable = '0' AND settle_flag = false;
                """, (trans_code_dim['deposit'], self.data['terminal_no'], return_code_dim['success']))['amount']
            self._increase_batch_no(self.data['terminal_no'])
            self._set_trace_no(self.data['terminal_no'], 1)
            self.db.execute("UPDATE trans SET settle_flag = true WHERE terminal_no = %s;", (self.data['terminal_no'],))
            self.db.commit()
            if (int(self.data['payment_count']) == int(payment_count)) and (int(self.data['payment_amount']) == int(payment_amount)) and (int(self.data['deposit_count']) == int(deposit_count))  and (int(self.data['deposit_amount']) == int(deposit_amount)):
                self.rtnData['result_code'] = return_code_dim['success']
            else:
                self.rtnData['result_code'] = return_code_dim['account_reconciliation']
            return self.rtnData
        except Exception, e:
            self.db.rollback()
            print "ERROR -> ", e.message
            self.rtnData['result_code'] = return_code_dim['unknown_error']
            return self.rtnData


    def cancel_trans(self):
        #
        #撤销
        #

        # 根据批次号和流水号确定原交易类型，根据确定的交易类型做撤销交易
        trans = self.db.fetch_one("SELECT * FROM trans WHERE card_no=%s AND terminal_no = %s AND batch_no = %s AND trace_no = %s;", 
                (self.data['card_no'], self.data['terminal_no'], self.data['old_batch_no'], self.data['old_trace_no'],))

        if not trans:
            self.rtnData['result_code'] = return_code_dim['cannot_fond_record']  # 交易记录未找到
            return self.rtnData
        else:
            reversiable = trans['reversiable']
            if reversiable == '1':
                self.rtnData['result_code'] = return_code_dim['canceled_trans']
                return self.rtnData
            elif reversiable == '2' or reversiable == '3':
                self.rtnData['result_code'] = return_code_dim['not_canceled_trans']
                return self.rtnData
            else:
                trans_code = trans['trans_code']
                if trans_code == trans_code_dim['payment']:
                    return self.cancel_payment()
                if trans_code == trans_code_dim['deposit']:
                    return self.cancel_deposit()
                if trans_code == trans_code_dim['points_payment']:
                    return self.cancel_points_payment()
                if trans_code == trans_code_dim['points_deposit']:
                    return self.cancel_points_deposit()

    def cancel_deposit(self):
        #
        # 充值撤销
        #
        self.rtnData['trans_code'] = trans_code_dim['cancel_deposit']
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查卡是否有效
        if not self._card_check():
            self._add_trans(reversiable='2')
            return self.rtnData
        # 找到上送的批次号和流水号的交易是否存在
        trans = self.db.fetch_one("SELECT * FROM trans WHERE card_no=%s AND trans_code = %s AND terminal_no = %s AND batch_no = %s AND trace_no = %s;", 
                (self.data['card_no'], trans_code_dim['deposit'], self.data['terminal_no'], self.data['old_batch_no'], self.data['old_trace_no'],))
        if not trans:
            self.rtnData['result_code'] = return_code_dim['cannot_fond_record']  # 交易记录未找到
        else:
            if trans['reversiable'] == '1':
                self.rtnData['result_code'] = return_code_dim['canceled_trans']
                self._add_trans(reversiable="2")
                return self.rtnData
            elif trans['reversiable'] == '2':
                self.rtnData['result_code'] = return_code_dim['not_canceled_trans']
                self._add_trans(reversiable="2")
                return self.rtnData
            else:
                old_amount = trans['amount']  # 原交易金额
                old_points = trans['points']  # 原交易积分
                if old_amount > int(self.card_info['amount']):  # 余额是否支持此次交易
                    self.rtnData['result_code'] = return_code_dim['balance_not_enough']
                    self._add_trans(reversiable="2")
                    return self.rtnData
                if old_points > int(self.card_info['points']):  # 卡内积分是否支持此次交易
                    self.rtnData['result_code'] = return_code_dim['points_not_enough']
                    self._add_trans(reversiable="2")
                    return self.rtnData
                try:
                    self.db.execute("UPDATE card_info SET amount = amount - %s, points = points - %s WHERE card_no = %s;",
                        (old_amount, old_points, self.data['card_no']))
                    self.db.execute("UPDATE trans SET reversiable='1' WHERE id = %s;", (trans['id'],))
                    self.rtnData['amount'] = -old_amount
                    self.rtnData['balance'] = int(self.card_info['amount'] - old_amount)
                    self.rtnData['current_points'] = - old_points
                    self.rtnData['total_points'] = int(self.card_info['points']) - old_points
                    self.rtnData['result_code'] = return_code_dim['success']
                    self._add_trans(reversiable="2", amount=old_amount)
                    return self.rtnData
                except Exception, e:
                    self.db.rollback()
                    self.rtnData['result_code'] = return_code_dim['unknown_error']
                    print "ERROR -> ", e.message
                    return self.rtnData

    def cancel_payment(self):
        #
        # 消费撤销
        #
        self.rtnData['trans_code'] = trans_code_dim['cancel_payment']
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查卡是否有效
        if not self._card_check():
            self._add_trans(reversiable='2')
            return self.rtnData
        # 找到上送的批次号和流水号的交易是否存在
        trans = self.db.fetch_one("SELECT * FROM trans WHERE card_no=%s AND trans_code = %s AND terminal_no = %s AND batch_no = %s AND trace_no = %s;", 
                (self.data['card_no'], trans_code_dim['payment'], self.data['terminal_no'], self.data['old_batch_no'], self.data['old_trace_no'],))
        if not trans:
            self.rtnData['result_code'] = return_code_dim['cannot_fond_record']  # 交易记录未找到
            return self.rtnData
        else:
            if trans['reversiable'] == '1':
                self.rtnData['result_code'] = return_code_dim['canceled_trans']
                self._add_trans(reversiable="2")
                return self.rtnData
            elif trans['reversiable'] == '2':
                self.rtnData['result_code'] = return_code_dim['not_canceled_trans']
                self._add_trans(reversiable="2")
                return self.rtnData
            else:
                old_amount = trans['amount']  # 原交易金额
                old_points = trans['points']  # 原交易积分
                # old_points_rule = trans['points_rule']
                if old_points > int(self.card_info['points']):  # 卡内积分是否支持此次交易
                    self.rtnData['result_code'] = return_code_dim['points_not_enough']
                    self._add_trans(reversiable="2")
                    return self.rtnData
                try:
                    self.db.execute("UPDATE card_info SET amount = amount + %s, points = points - %s WHERE card_no = %s;",
                        (old_amount, old_points, self.data['card_no']))
                    self.db.execute("UPDATE trans SET reversiable='1' WHERE id = %s;", (trans['id'],))
                    self.rtnData['amount'] = old_amount
                    self.rtnData['balance'] = int(self.card_info['amount'] + old_amount)
                    self.rtnData['current_points'] = - old_points
                    self.rtnData['total_points'] = int(self.card_info['points']) - old_points
                    self.rtnData['result_code'] = return_code_dim['success']
                    self._add_trans(reversiable="2", points_rule=0, points=old_points, amount=old_amount)
                    return self.rtnData
                except Exception, e:
                    self.db.rollback()
                    self.rtnData['result_code'] = return_code_dim['unknown_error']
                    print "ERROR -> ", e.message
                    return self.rtnData
    
    def cancel_points_deposit(self):
        #
        # 积分充值撤销
        #
        self.rtnData['trans_code'] = trans_code_dim['cancel_points_deposit']
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查卡是否有效
        if not self._card_check():
            self._add_trans(reversiable='2')
            return self.rtnData
        # 找到上送的批次号和流水号的交易是否存在
        trans = self.db.fetch_one("SELECT * FROM trans WHERE card_no=%s AND trans_code = %s AND terminal_no = %s AND batch_no = %s AND trace_no = %s;", 
                (self.data['card_no'], trans_code_dim['points_deposit'], self.data['terminal_no'], self.data['old_batch_no'], self.data['old_trace_no'],))
        if not trans:
            self.rtnData['result_code'] = return_code_dim['cannot_fond_record']  # 交易记录未找到
            return self.rtnData
        else:
            if trans['reversiable'] == '1':
                self.rtnData['result_code'] = return_code_dim['canceled_trans']
                self._add_trans(reversiable="2")
                return self.rtnData
            elif trans['reversiable'] == '2':
                self.rtnData['result_code'] = return_code_dim['not_canceled_trans']
                self._add_trans(reversiable="2")
                return self.rtnData
            else:
                old_points = trans['amount']  # 原交易积分
                if old_points > int(self.card_info['points']):  # 卡内积分是否支持此次交易
                    self.rtnData['result_code'] = return_code_dim['points_not_enough']
                    self._add_trans(reversiable="2")
                    return self.rtnData

                try:
                    self.db.execute("UPDATE card_info SET points = points - %s WHERE card_no = %s;",
                        (old_points, self.data['card_no']))
                    self.db.execute("UPDATE trans SET reversiable='1' WHERE id = %s;", (trans['id'],))
                    self.rtnData['amount'] = '0.00'
                    self.rtnData['balance'] = int(self.card_info['amount'])
                    self.rtnData['current_points'] = - old_points
                    self.rtnData['total_points'] = int(self.card_info['points']) - old_points
                    self.rtnData['result_code'] = return_code_dim['success']
                    self._add_trans(reversiable="2", points=old_points)
                    return self.rtnData
                except Exception, e:
                    self.db.rollback()
                    self.rtnData['result_code'] = return_code_dim['unknown_error']
                    print "ERROR -> ", e.message
                    return self.rtnData

    def cancel_points_payment(self):
        #
        # 积分消费撤销
        #
        self.rtnData['trans_code'] = trans_code_dim['cancel_points_payment']
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData
        # 检查卡是否有效
        if not self._card_check():
            self._add_trans(reversiable='2')
            return self.rtnData
        # 找到上送的批次号和流水号的交易是否存在
        trans = self.db.fetch_one("SELECT * FROM trans WHERE card_no=%s AND trans_code = %s AND terminal_no = %s AND batch_no = %s AND trace_no = %s;", 
                (self.data['card_no'], trans_code_dim['points_payment'], self.data['terminal_no'], self.data['old_batch_no'], self.data['old_trace_no'],))
        if not trans:
            self.rtnData['result_code'] = return_code_dim['cannot_fond_record']  # 交易记录未找到
            return self.rtnData
        else:
            if trans['reversiable'] == '1':
                self.rtnData['result_code'] = return_code_dim['canceled_trans']
                self._add_trans(reversiable="2")
                return self.rtnData
            elif trans['reversiable'] == '2':
                self.rtnData['result_code'] = return_code_dim['not_canceled_trans']
                self._add_trans(reversiable="2")
                return self.rtnData
            else:
                old_points = trans['amount']  # 原交易积分                
                try:
                    self.db.execute("UPDATE card_info SET points = points + %s WHERE card_no = %s;",
                        (old_points, self.data['card_no']))
                    self.db.execute("UPDATE trans SET reversiable='1' WHERE id = %s;", (trans['id'],))
                    self.rtnData['amount'] = '0.00'
                    self.rtnData['balance'] = int(self.card_info['amount'])
                    self.rtnData['current_points'] = old_points
                    self.rtnData['total_points'] = int(self.card_info['points']) + old_points
                    self.rtnData['result_code'] = return_code_dim['success']
                    self._add_trans(reversiable="2", points=old_points)
                    return self.rtnData
                except Exception, e:
                    self.db.rollback()
                    self.rtnData['result_code'] = return_code_dim['unknown_error']
                    print "ERROR -> ", e.message
                    return self.rtnData                    

    def reversal(self):
        #
        # 冲正
        #
        self.rtnData['trans_code'] = trans_code_dim['reversal']
        # 检查商户号与终端号
        if not self._is_shop_terminal_valid(self.data['shop_no'], self.data['terminal_no']):
            return self.rtnData
        # 检查批次号和流水号
        if not self._batch_no_trace_no_check(self.data['batch_no'], self.data['trace_no'], self.data['terminal_no']):
            return self.rtnData

        # 检查是否是本集团卡
        if not self._is_my_unit_card(self.data['shop_no'], self.data['card_no']):
            self.rtnData['result_code'] = return_code_dim['outward_card']
            self._add_trans(reversiable='2')
            return self.rtnData

        # 检查卡是否有效
        if not self._card_check():
            self._add_trans(reversiable='2')
            return self.rtnData

        # 可以冲正的交易:消费、消费撤销、充值、充值撤销、积分消费、积分消费撤销、积分充值、积分充值撤销
        # 根据批次号和流水号来确定一笔被冲正的交易
        trans = self.db.fetch_one("SELECT * FROM trans WHERE card_no=%s AND terminal_no = %s AND batch_no = %s AND trace_no = %s;", 
                (self.data['card_no'], self.data['terminal_no'], self.data['old_batch_no'], self.data['old_trace_no'],))        

        if not trans:
            self.rtnData['result_code'] = return_code_dim['success']
            return self.rtnData
        else:
            if trans['reversiable'] == '1':
                self.rtnData['result_code'] = return_code_dim['canceled_trans']
                self._add_trans(reversiable="2")
                return self.rtnData
            elif trans['reversiable'] in  ('2', '3'):
                self.rtnData['result_code'] = return_code_dim['not_canceled_trans']
                self._add_trans(reversiable="2")
                return self.rtnData
            else:
                old_id = trans['id']
                old_card_no = trans['card_no']
                old_amount = trans['amount']  # 原交易金额
                old_points = trans['points']  # 原交易积分
                old_points_rule = trans['points_rule']  # 原积分规则
                try:
                    if trans['trans_code'] == trans_code_dim['payment']:  # 消费交易的冲正
                        if old_amount > int(self.card_info['amount']):  # 余额是否支持此次交易
                            self.rtnData['result_code'] = return_code_dim['balance_not_enough']
                            self._add_trans(reversiable="2")
                            return self.rtnData
                        if old_points > int(self.card_info['points']):  # 卡内积分是否支持此次交易
                            self.rtnData['result_code'] = return_code_dim['points_not_enough']
                            self._add_trans(reversiable="2")
                            return self.rtnData

                        self.db.execute("UPDATE card_info SET amount = amount - %s, points = points - %s WHERE card_no = %s;",
                            (old_amount, old_points, old_card_no))
                        self.db.execute("UPDATE trans SET reversiable = '3' WHERE id = %s;", (old_id,))
                        self.rtnData['amount'] = -old_amount
                        self.rtnData['balance'] = int(self.card_info['amount'] - old_amount)
                        self.rtnData['current_points'] = - old_points
                        self.rtnData['total_points'] = int(self.card_info['points']) - old_points
                        self.rtnData['result_code'] = return_code_dim['success']
                        self._add_trans(reversiable="2", points_rule=old_points_rule, points=old_points, amount=old_amount)
                        return self.rtnData

                    if trans['trans_code'] == trans_code_dim['cancel_payment']:  # 消费撤销交易的冲正
                        if old_amount > int(self.card_info['amount']):  # 余额是否支持此次交易
                            self.rtnData['result_code'] = return_code_dim['balance_not_enough']
                            self._add_trans(reversiable="2")
                            return self.rtnData

                        self.db.execute("UPDATE card_info SET amount = amount - %s, points = points + %s WHERE card_no = %s;",
                            (old_amount, old_points, old_card_no))
                        self.db.execute("UPDATE trans SET reversiable = '3' WHERE id = %s;", (old_id,))
                        self.rtnData['amount'] = -old_amount
                        self.rtnData['balance'] = int(self.card_info['amount'] - old_amount)
                        self.rtnData['current_points'] = old_points
                        self.rtnData['total_points'] = int(self.card_info['points']) + old_points
                        self.rtnData['result_code'] = return_code_dim['success']
                        self._add_trans(reversiable="2", points_rule=old_points_rule, points=old_points, amount=old_amount)
                        return self.rtnData

                    if trans['trans_code'] == trans_code_dim['deposit']:  # 充值交易的冲正
                        if old_amount > int(self.card_info['amount']):  # 余额是否支持此次交易
                            self.rtnData['result_code'] = return_code_dim['balance_not_enough']
                            self._add_trans(reversiable="2")
                            return self.rtnData

                        self.db.execute("UPDATE card_info SET amount = amount - %s, points = points - %s WHERE card_no = %s;",
                            (old_amount, old_points, old_card_no))
                        self.db.execute("UPDATE trans SET reversiable = '3' WHERE id = %s;", (old_id,))
                        self.rtnData['amount'] = -old_amount
                        self.rtnData['balance'] = int(self.card_info['amount'] - old_amount)
                        self.rtnData['current_points'] = - old_points
                        self.rtnData['total_points'] = int(self.card_info['points']) - old_points
                        self.rtnData['result_code'] = return_code_dim['success']
                        self._add_trans(reversiable="2", points_rule=old_points_rule, points=old_points, amount=old_amount)
                        return self.rtnData

                    if trans['trans_code'] == trans_code_dim['cancel_deposit']:  # 充值撤销交易的冲正
                        self.db.execute("UPDATE card_info SET amount = amount + %s, points = points + %s WHERE card_no = %s;",
                            (old_amount, old_points, old_card_no))
                        self.db.execute("UPDATE trans SET reversiable = '3' WHERE id = %s;", (old_id,))
                        self.rtnData['amount'] = -old_amount
                        self.rtnData['balance'] = int(self.card_info['amount'] + old_amount)
                        self.rtnData['current_points'] =  old_points
                        self.rtnData['total_points'] = int(self.card_info['points']) + old_points
                        self.rtnData['result_code'] = return_code_dim['success']
                        self._add_trans(reversiable="2", points_rule=old_points_rule, points=old_points, amount=old_amount)
                        return self.rtnData
                
                    if trans['trans_code'] == trans_code_dim['points_payment']:  # 积分消费交易的冲正
                        self.db.execute("UPDATE card_info SET points = points + %s WHERE card_no = %s;",
                            (old_points, old_card_no))
                        self.db.execute("UPDATE trans SET reversiable = '3' WHERE id = %s;", (old_id,))
                        self.rtnData['amount'] = '0.00'
                        self.rtnData['balance'] = int(self.card_info['amount'])
                        self.rtnData['current_points'] =  old_points
                        self.rtnData['total_points'] = int(self.card_info['points']) + old_points
                        self.rtnData['result_code'] = return_code_dim['success']
                        self._add_trans(reversiable="2", points_rule=old_points_rule, points=old_points)
                        return self.rtnData

                    if trans['trans_code'] == trans_code_dim['cancel_points_payment']:  # 积分消费撤销交易的冲正
                        if old_points > int(self.card_info['points']):  # 卡内积分是否支持此次交易
                            self.rtnData['result_code'] = return_code_dim['points_not_enough']
                            self._add_trans(reversiable="2")
                            return self.rtnData
                        self.db.execute("UPDATE card_info SET points = points - %s WHERE card_no = %s;",
                            (old_points, old_card_no))
                        self.db.execute("UPDATE trans SET reversiable = '3' WHERE id = %s;", (old_id,))
                        self.rtnData['amount'] = '0.00'
                        self.rtnData['balance'] = int(self.card_info['amount'])
                        self.rtnData['current_points'] = - old_points
                        self.rtnData['total_points'] = int(self.card_info['points']) - old_points
                        self.rtnData['result_code'] = return_code_dim['success']
                        self._add_trans(reversiable="2", points_rule=old_points_rule, points=old_points)
                        return self.rtnData

                    if trans['trans_code'] == trans_code_dim['points_deposit']:  # 积分充值交易的冲正
                        if old_points > int(self.card_info['points']):  # 卡内积分是否支持此次交易
                            self.rtnData['result_code'] = return_code_dim['points_not_enough']
                            self._add_trans(reversiable="2")
                            return self.rtnData
                        self.db.execute("UPDATE card_info SET points = points - %s WHERE card_no = %s;",
                            (old_points, old_card_no))
                        self.db.execute("UPDATE trans SET reversiable = '3' WHERE id = %s;", (old_id,))
                        self.rtnData['amount'] = '0.00'
                        self.rtnData['balance'] = int(self.card_info['amount'])
                        self.rtnData['current_points'] = - old_points
                        self.rtnData['total_points'] = int(self.card_info['points']) - old_points
                        self.rtnData['result_code'] = return_code_dim['success']
                        self._add_trans(reversiable="2", points_rule=old_points_rule, points=old_points)
                        return self.rtnData

                    if trans['trans_code'] == trans_code_dim['cancel_points_deposit']:  # 积分充值撤销交易的冲正
                        self.db.execute("UPDATE card_info SET points = points + %s WHERE card_no = %s;",
                            (old_points, old_card_no))
                        self.db.execute("UPDATE trans SET reversiable = '3' WHERE id = %s;", (old_id,))
                        self.rtnData['amount'] = '0.00'
                        self.rtnData['balance'] = int(self.card_info['amount'])
                        self.rtnData['current_points'] = old_points
                        self.rtnData['total_points'] = int(self.card_info['points']) + old_points
                        self.rtnData['result_code'] = return_code_dim['success']
                        self._add_trans(reversiable="2", points_rule=old_points_rule, points=old_points)
                        return self.rtnData
                except Exception, e:
                    self.db.rollback()
                    self.rtnData['result_code'] = return_code_dim['unknown_error']
                    print "ERROR -> ", e.message
                    return self.rtnData
