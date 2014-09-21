# -*- coding=utf-8 -*-
import sys
import psycopg2
import psycopg2.extras
import datetime
import time

def GetData(pg_conn=None, sql='', vars=()):
    sql = sql.strip()
    if (not pg_conn) or (not sql):
        return None
        
    pg_cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    pg_cursor.execute(sql, vars)
    return pg_cursor.fetchall()


def GetCount(pg_conn=None, sql='', vars=()):
    count = GetData(pg_conn, sql, vars)
    if count == None:
        return 0
    return count[0][0]    


pg_db = 'jf_card'  # 数据库名
pg_host = 'localhost'  # 数据库主机
pg_user = 'postgres'  #数据库用户名
pg_password = '123456'  # 数据库密码

trans_code = ( # 要计入交易统计表的交易类型
    '000010',  # 消费 
    '000110',  # 启用
    '000030',  # 充值
    '000050',  # 积分消费
    '000070',  # 积分充值
    '000020',  # 消费撤销
    '000040',  # 充值撤销
    '000060',  # 积分消费撤销
    '000080'   # 积分充值撤销
    )

rz_date = time.strftime('%Y%m%d',time.localtime(time.time()))  # 日终日期

# 数据库连接
pg_conn = psycopg2.connect(database=pg_db, user=pg_user, password=pg_password, host=pg_host)
pg_cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


# 更新集团账户表数据
sql = """
    INSERT INTO report_unit_account(unit_no, rz_date)
    (SELECT unit_no, to_date(to_char(now(), 'YYYYMMDD'), 'YYYYMMDD') FROM unit_info ORDER BY unit_no)
    """
pg_cursor.execute(sql, ())

sql = """
    SELECT unit_no, COUNT(*) count, SUM(amount) amount, status FROM card_info
    GROUP BY unit_no, status
    ORDER BY unit_no
    """
accounts = GetData(pg_conn, sql)
for account in accounts:
    if account['status'] == '0':
        sql = "UPDATE report_unit_account SET new_count = %s, new_amount = %s WHERE unit_no = %s AND rz_date = %s;"
    elif account['status'] == '1':
        sql = "UPDATE report_unit_account SET normal_count = %s, normal_amount = %s WHERE unit_no = %s AND rz_date = %s;"
    elif account['status'] == '2':
        sql = "UPDATE report_unit_account SET lost_count = %s, lost_amount = %s WHERE unit_no = %s AND rz_date = %s;"
    elif account['status'] == '3':
        sql = "UPDATE report_unit_account SET frozen_count = %s, frozen_amount = %s WHERE unit_no = %s AND rz_date = %s;"
    elif account['status'] == '4':
        sql = "UPDATE report_unit_account SET invalid_count = %s, invalid_amount = %s WHERE unit_no = %s AND rz_date = %s;"
    pg_cursor.execute(sql, (account['count'], account['amount'], account['unit_no'], rz_date))
# 对交易统计表进行统计
# 方法: 从商户表中取出所有商户, 对每个商户进行统计.统计时要区分交易类型
# 如果昨日因为谋职谋职某种原因没有成功,本次继续日终
dates = GetData(pg_conn, "SELECT DISTINCT trans_date FROM trans;")
for date in dates:
    trans_date = date['trans_date']
    # 更新账户统计表数据
    sql = """
        INSERT INTO report_statistic (trans_count, trans_amount, credit_unit, debit_unit, shop_no, trans_code, trans_date)
            (
                SELECT COUNT(*), SUM(amount), credit_unit, debit_unit, shop_no, trans_code, trans_date 
                FROM  trans
                WHERE result_code='0' AND cx_flag='0' AND trans_date = %s AND trans_code IN %s
                GROUP BY credit_unit, debit_unit, shop_no, trans_code, trans_date
            );

        """
    vars = (trans_date, trans_code)
    pg_cursor.execute(sql, vars)

    
    # 将交易从当日交易表转存到历史交易表中
    sql ="""
        INSERT INTO history_trans(id, card_no, terminal_no, trans_code, trans_date, trans_time, result_code, cx_flag, points_rule,
            amount, points, shop_no, credit_unit, debit_unit, batch_no, trace_no, pos_operator, amount_balance, points_balance)
        (SELECT id, card_no, terminal_no, trans_code, trans_date, trans_time, result_code, cx_flag, points_rule,
            amount, points, shop_no, credit_unit, debit_unit, batch_no, trace_no, pos_operator, amount_balance, points_balance
            FROM trans
            WHERE trans_date = %s);
        """
    pg_cursor.execute(sql, (trans_date, ))

    # 删除当日交易表中的数据
    pg_cursor.execute("DELETE FROM trans WHERE trans_date=%s;", (trans_date, ))

pg_cursor.close()
pg_conn.commit()    
