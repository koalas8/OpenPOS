#-*- coding=utf-8 -*
import rspmsg
import uuid
import ConfigParser
import socket
from flask import Flask, g, session, redirect, url_for, request, render_template, abort
from flask.json import jsonify
from flask.views import MethodView
from modules import *
from sqlalchemy import or_
from ccard.protocols.trans.Trans_pb2 import Trans

app = Flask(__name__)
app.secret_key = 'adafdasdfdasfads'


def get_config(section, option):
    # 从配置文件中读取配置
    cf = ConfigParser.ConfigParser()
    cf.read('config.cfg')
    return cf.get(section=section, option=option)


SOCKET_SERVER = get_config('NET', 'WEBTRANS_SERVER')
SOCKET_PORT = int(get_config('NET', 'WEBTRANS_PORT'))


def send_socket_message(msg):
    # 以socket方式发送交易数据并接收返回
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    s.connect((SOCKET_SERVER, SOCKET_PORT))
    s.send(msg)
    data = s.recv(4096)
    return data


@app.before_request
def check_login():
    session['user_no'] = '0000'
    session['user_level'] = 'terminal'
    session['unit_no'] = '0000'
    session['shop_no'] = '999031100000001'
    session['default_terminal_no'] = '00000000'


@app.route('/index')
def index():
    return render_template('angtrans_index.html')


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = ''
        q = db_session.query(UserInfo).filter(UserInfo.user_no == username)
        q = db_session.query(UserInfo).filter(UserInfo.user_level == 'terminal')
        if not q.count():
            error = rspmsg.USER_DONOT_EXIST
        else:
            user = q.filter(UserInfo.user_no == username).first()
            if user.password != md5(password).digest():
                error = rspmsg.WRONG_PASSWORD
            else:
                session['user_no'] = user.user_no
                session['user_level'] = user.user_level
                session['unit_no'] = user.unit_no
                session['shop_no'] = user.shop_no

                q = db_session.query(TerminalInfo)
                q = q.filter(TerminalInfo.shop_no == session['shop_no'])
                q = q.filter(TerminalInfo.is_default == True)
                if q.count():
                    session['default_terminal_no'] = q.one().terminal_no
                else:
                    session['default_terminal_no'] = ''

                return render_template('angtrans_index.html')
        return render_template('login.html', error=error)


class City(MethodView):
    def get(self):
        pid = request.args.get('pid', '0').strip()
        cities = db_session.query(SysCityDim.id, SysCityDim.city).filter(SysCityDim.pid == pid).all()
        return jsonify(success=True, total=1, page=1, limit=9999,
                       data=[{'id': c.id, 'city': c.city} for c in cities])


app.add_url_rule('/city', view_func=City.as_view('city'))


class Member(MethodView):
    def post(self):
        input = request.json
        card_no, member_name = input.get('card_no', '').strip(), input.get('member_name', '').strip()  # 两个必填项
        member_level = input.get('member_level', '').strip()
        sex = input.get('sex', '男').strip()
        id_card = input.get('id_card', '').strip()
        phone = input.get('phone', '').strip()
        birthday = input.get('birthday', '').strip()
        email = input.get('email', '').strip()
        province = input.get('province', None)
        city = input.get('city', None)
        district = input.get('district', None)
        country = input.get('country', None)
        address = input.get('address', '')

        if not card_no or not member_name:
            return jsonify(success=False, msg=u'卡号或会员姓名不能为空')

        # 检查卡号是否存在，并且已经登记了会员
        q = db_session.query(CardInfo).filter(CardInfo.card_no == card_no).filter(
            CardInfo.unit_no == session['unit_no'])
        if not q.count():
            return jsonify(success=False, msg=u'卡号不存在')

        card = q.first()
        member_id = card.member_id
        if member_id:
            return jsonify(success=False, msg=u'此卡已登记会员信息')

        # 登记会员
        id = str(uuid.uuid4())
        member = MemberInfo(id=id, unit_no=session['unit_no'], shop_no=session['shop_no'], member_name=member_name,
                            sex=sex, birthday=birthday, phone=phone, email=email, address=address, idcard=id_card,
                            province=province, city=city, district=district, country=country)
        card.member_id = id
        db_session.add(member)
        db_session.add(card)
        db_session.commit()

        return jsonify(success=True, msg=u'添加会员成功')


class MemberList(MethodView):
    def get(self):
        input = request.args
        keyword = input.get('keyword', '').strip()
        limit = int(input.get('limit', '20').strip())
        page = int(input.get('page', '1').strip())

        q = db_session.query(MemberInfo).filter(MemberInfo.unit_no == session['unit_no'])
        if keyword:
            q.filter(
                or_(MemberInfo.member_name.like('%' + keyword + '%'), MemberInfo.card_no.like('%' + keyword + '%')))
        total = q.count()
        members = q.limit(limit).offset((page - 1) * limit).all()
        return jsonify(success=True, total=total, page=page, limit=limit,
                       data=[{'member_name': m.member_name, 'sex': m.sex, 'phone': m.phone, } for m in members])


app.add_url_rule('/member', view_func=Member.as_view('member'))
app.add_url_rule('/member/list', view_func=MemberList.as_view('member_list'))


class WebTrans(MethodView):
    def post(self):
        # 是否有默认终端?
        if not session['default_terminal_no']:
            return jsonify(success=False, msg=u'无默认终端,请先设置默认终端')
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

        trans = Trans()
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
            trans.terminal_no = session['default_terminal_no']
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
            trans.track_2 = input.get('track_2', '')
        # 新卡的二磁道（补卡交易时用）
        if action in ['000120']:
            trans.new_card_track_2 = input.get('new_track_2', '')
        # 卡密码
        if action in ['000010', '000020', '000030', '000040', '000050', '000060',
                      '000070', '000080', '000090', '000110', '000120', '000140',
                      '000150']:
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

        trans_string = trans.SerializeToString()
        trans_result = eval(send_socket_message(trans_string))

        result_code = trans_result.get('result_code', '')

        if result_code != '0':
            error = get_result_message(result_code)
            return jsonify(success=False, msg=error)

        ##
        # 小票变量
        shop_no = trans_result.get('shop_no', '')
        shop_name = trans_result.get('shop_name', '')
        terminal_no = trans_result.get('terminal_no', '')
        operator_no = session.operator_no
        card_no = trans_result.get('card_no', '')
        trans_date = trans_result.get('trans_date', '')
        trans_time = trans_result.get('trans_time', '')
        batch_no = trans_result.get('batch_no', '')
        trace_no = trans_result.get('trace_no', '')
        trans_name = get_trans_name(trans_result['action'])
        amount = int(trans_result.get('amount', 0.00))
        balance = int(trans_result.get('balance', 0.00))
        current_points = trans_result.get('current_points', 0.00)
        total_points = trans_result.get('total_points', 0.00)
        ticket_result = trans_result.get('result_code', '')
        ticket = render_template('web_trans/trans/ticket.html', **locals())

        ##
        # 小票文本
        ticket = render_template('angtrans/ticket.tpl',
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

        return jsonify(success=True, data={'ticket': ticket, 'print_text': print_text})


app.add_url_rule('/webtrans', view_func=WebTrans.as_view('web_trans'))


class Order(MethodView):
    def post(self):
        pass


class Pay(MethodView):
    def post(self):
        pass
