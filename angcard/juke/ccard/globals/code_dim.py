#-*- coding=utf-8 -*-

def get_trans_code(en_name):
    trans_code_dim = {
        'singin'                : '000000',  # 签到 
        'payment'               : '000010',  # 消费
        'cancel_payment'        : '000020',  # 消费撤销
        'deposit'               : '000030',  # 充值
        'cancel_deposit'        : '000040',  # 充值撤销
        'points_payment'        : '000050',  # 积分消费
        'cancel_points_payment' : '000060',  # 积分消费撤销
        'points_deposit'        : '000070',  # 积分充值
        'cancel_points_deposit' : '000080',  # 积分充值撤销
        'check_balance'         : '000090',  # 查询卡余额
        'check_points'          : '000100',  # 查询
        'new_card'              : '000110',  # 卡启用
        'change_card'           : '000120',  # 换卡
        'write_card'            : '000130',  # 补磁
        'change_password'       : '000140',  # 卡改密码
        'change_overdue_date'   : '000150',  # 卡改有效期
        'reversal'              : '000160',  # 冲正    
        'unknown'               : '000170',  # 未知
        'settlement'            : '000180',  # 结算
        'cancel_trans'          : '000190',  # 撤销(消费、充值、积分消费、积分充值的撤销)
        'bind_member'           : '100010'
    }
    return trans_code_dim.get(en_name, '')


def get_return_code(en_name):
    return_code_dim = {
        'success'                   : '0',   # 成功
        'shop_not_exist'            : '2',   # 商户号不存在
        'terminal_not_exist'        : '3',   # 终端号不存在
        'lost_card'                 : '4',   # 挂失卡
        'disabled_card'             : '5',   # 冻结卡
        'invalid_card'              : '6',   # 作废卡
        'overdue_card'              : '7',   # 过期卡
        'outward_card'              : '8',   # 非本系统卡
        'not_my_card'               : '9',   # 非本集团卡
        'invalid_card_no'           : '10',  # 无效卡号
        'new_card'                  : '11',  # 新卡未启用
        'enabled_card'              : '12',  # 卡已启用
        'unknown_error'             : '13',  # 未知错误
        'wrong_password'            : '14',  # 密码错
        'database_error'            : '15',  # 数据库错误
        'invalid_balance'           : '16',  # 无效金额
        'balance_not_enough'        : '17',  # 余额不足
        'cannot_fond_record'        : '18',  # 交易记录未找到
        'invalid_points'            : '19',  # 无效积分
        'points_not_enough'         : '20',  # 积分不足
        'canceled_trans'            : '21',  # 交易已取消
        'not_canceled_trans'        : '22',  # 原交易不能取消
        'illegal_card'              : '23',  # 非法卡
        'invalid_batch_no'          : '24',  # 批次号错
        'invalid_trace_no'          : '25',  # 流水号错
        'operator_not_exist'        : '26',  # POS操作员不存在
        'wrong_operator_pwd'        : '27',  # POS操作员密码错
        'frozen_operator'           : '28',  # POS操作员已冻结
        'account_reconciliation'    : '29',  # 账不平
        'forbidden_card_feature'    : '30',  # 该卡无此功能
        'forbidden_terminal_trans'  : '31',  # 终端无此权限
        'invalid_amount_format'     : '32',  # 金额格式不正确
        'invalid_date_format'       : '33',  # 日期格式不正确
        'binded_card'               : '61',  # 卡已经绑定
    }
    return return_code_dim.get(en_name, '')


def get_interface_code(en_name):
    INTERFACE = {'desktop_soft': '0', 'web': '1'}
    return INTERFACE.get(en_name, '')


def get_trans_name(code):
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
        '000090': u'查询卡余额',
        '000100': u'查询',
        '000110': u'卡启用',
        '000120': u'换卡',
        '000130': u'补磁',
        '000140': u'卡改密码',
        '000150': u'卡改有效期',
        '000160': u'冲正    ',
        '000170': u'未知',
        '000180': u'结算',
        '100010': u'返回码信息'
        }
    return trans_code_dim.get(code, '')

def get_result_message(code):
    return_code_dim = {
        '0': u'成功',
        '2': u'商户号不存在',
        '3': u'终端号不存在',
        '4': u'挂失卡',
        '5': u'冻结卡',
        '6': u'作废卡',
        '7': u'过期卡',
        '8': u'非本系统卡',
        '9': u'非本集团卡',
        '10': u'无效卡号',
        '11': u'新卡未启用',
        '12': u'卡已启用',
        '13': u'未知错误',
        '14': u'密码错',
        '15': u'数据库错误',
        '16': u'无效金额',
        '17': u'余额不足',
        '18': u'交易记录未找到',
        '19': u'无效积分',
        '20': u'积分不足',
        '21': u'交易已取消',
        '22': u'原交易不能取消',
        '23': u'非法卡',
        '24': u'批次号错',
        '25': u'流水号错',
        '26': u'POS操作员不存在',
        '27': u'POS操作员密码错',
        '28': u'POS操作员已冻结',
        '29': u'账不平',
        '30': u'该卡无此功能',
        '31': u'终端无此权限',
        '32': u'金额格式不正确',
        '33': u'日期格式不正确',
        '61': u'卡已经绑定'
    }
    return return_code_dim.get(code, '')