#-*- coding=utf-8 -*-

############################# SESSION 项 ###############################
# session['unit_no']
# session['shop_no']
# session['default_terminal']
# session['purchase_order_id']  采购单ID，提交采购单后要删除此session值
# session['sina_weibo_uid']
# session['sina_weibo_token']
# session['app_type'] : 0:通用 1:鞋服

#################### 用户项 #############################################
# 1.系统用户是有集团号和登陆账号确定的，所以数据库表中的user_no列是可以重复的
# 2.因为第一条的存在：
#   a.注册时，用户名可以在整个数据表中重复，但不能在同一集团下重复
#   b.
import importlib
from flask import Flask
from flask import make_response
from flask.ext import restful

app = Flask(__name__)
app.config.from_object('juke.config.DevelopmentConfig')
#app.config.from_object('juke.config.ProductionConfig')

api = restful.Api(app)


## 设置一下flask-restful, 使其可以支持返回 text/html 类型数据
@api.representation('text/html')
def html(data, code, headers=None):
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp

## 开启日志
import logging
file_handler = logging.FileHandler('log.txt')
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

urls = [
    ## 用户
    ('/captcha', 'juke.views.users.Captcha'),  # 验证码
    ('/', '/login', 'juke.views.users.Login'),  # 登录
    ('/logout', 'juke.views.users.Logout'),  # 登出
    ('/index', 'juke.views.users.Index'),  # 主页
    ('/user/register', 'juke.views.users.Register'),  # 注册
    ('/user/register/check', 'juke.views.users.RegisterCheck'),
    ('/user', 'juke.views.users.UserList'),  # 用户列表
    ('/user/<string:user_no>', 'juke.views.users.User'),  # 用户明细、修改、删除
    ('/user/operations', 'juke.views.users.UserOperations'),  # 获取当前系统用户权限
    ('/user/profile', 'juke.views.users.MyProfile'),
    ('/settings/account', 'juke.views.users.UserAccount'),  # 用户账号设置

    ## 卡
    ('/card', 'juke.views.card.CardList'),
    ('/card/<string:card_no>', 'juke.views.card.Card'),
    ('/card/<string:card_no>/trans', 'juke.views.card.CardTrans'),
    ('/card/group', 'juke.views.card.CardGroupList'),
    ('/card/group/<group_id>', 'juke.views.card.CardGroup'),

    ## 会员
    ('/member/<member_id>/card', 'juke.views.member.MemberCardList'),  # 会员持卡
    ('/member', 'juke.views.member.MemberList'),  # 会员列表

    ## 集团
    ('/unit', 'juke.views.orgs.UnitList'),
    ('/unit/<string:unit_no>', 'juke.views.orgs.Unit'),
    ('/unit/inter', 'juke.views.orgs.UnitInterList'),
    ('/unit/inter/<string:inter_id>', 'juke.views.orgs.UnitInter'),

    ## 商户
    ('/shop', 'juke.views.orgs.ShopList'),
    ('/shop/<string:shop_no>', 'juke.views.orgs.Shop'),

    ## 终端
    ('/terminal', 'juke.views.orgs.TerminalList'),
    ('/terminal/default', 'juke.views.webpos.DefaultTerminal'),
    ('/terminal/<string:terminal_no>', 'juke.views.orgs.Terminal'),
    ('/terminal/trans/code', 'juke.views.orgs.TerminalTransCodes'),

    ## 报表
    ('/report/balance', 'juke.views.reports.BalanceReport'),
    ('/report/unit/mx', 'juke.views.reports.UnitMxReport'),
    ('/report/shop/mx', 'juke.views.reports.ShopMxReport'),
    ('/report/terminal/mx', 'juke.views.reports.TerminalMxReport'),

    ## 权限
    ('/role', 'juke.views.roles.RoleList'),
    ('/role/grant', 'juke.views.roles.RoleGrantList'),
    ('/role/operations', 'juke.views.roles.RoleOperations'),

    ## webpos
    ('/webtrans', 'juke.views.webpos.WebTrans'),

    ## 商品
    # ('/size/group', 'juke.views.psi.size.SizeGroupList'),
    ('/goods/info/base', 'juke.views.psi.goods.GoodsBaseInfoList'),  # 商品基本信息维护
    ('/goods/info/base/<string:goods_id>', 'juke.views.psi.goods.MyGoodsBaseInfo'),  # GoodsBaseInfo 与数据库冲突 商品基本信息维护
    ('/goods', 'juke.views.psi.goods.GoodsList'),  # 商品详细信息
    ('/goods/<string:goods_id>', 'juke.views.psi.goods.Goods'),  # 商品详细信息维护
    ## --> 品牌管理
    ('/goods/brand', 'juke.views.psi.brand.BrandList'),
    ('/goods/brand/<string:brand_id>', 'juke.views.psi.brand.Brand'),
    ## --> 商品分类
    ('/goods/class', 'juke.views.psi.goods.GoodsClassList'),
    ## --> 商品采购
    ('/goods/purchase/order', 'juke.views.psi.goods.PurchaseOrderList'),

    ## 销售订单
    ('/sale/order', 'juke.views.psi.sale.OrderList'),
    ('/sale/order/detail/<order_id>', 'juke.views.psi.sale.OrderDetail'),
    ('/sale/order/<string:order_id>', '/sale/order/<string:order_id>/<string:action>', 'juke.views.psi.sale.Order'),
    ('/sale/income', 'juke.views.psi.sale.Income'),
    ('/sale/report', 'juke.views.psi.sale.SoldGoodsReport'),

    ## 供应商
    ('/supplier', 'juke.views.psi.supplier.SupplierList'),
    ('/supplier/<string:supplier_id>', 'juke.views.psi.supplier.Supplier'),

    ## 仓库
    ('/warehouse', 'juke.views.psi.warehouse.WarehouseList'),
    ('/warehouse/<string:warehouse_id>', 'juke.views.psi.warehouse.Warehouse'),
    ('/warehouse/recepit', 'juke.views.psi.warehouse.WarehouseReceiptList'),

    ## 微博
    ('/weibo/sina/bind', 'juke.views.SNS.sinaweibo.SinaWeiboBinding'),
    # ('/weibo/sina/reg', 'juke.views.SNS.sinaweibo.SinaWeiboRegister'),
    ('/weibo/sina/login', 'juke.views.SNS.sinaweibo.SinaWeiboLogin'),
    ('/weibo/sina/login/callback', 'juke.views.SNS.sinaweibo.SinaWeiboLoginCallback')
]

for url in urls:
    # try:
    mod, cls = url[-1].rsplit('.', 1)
    mod = importlib.import_module(mod)
    cls = getattr(mod, cls)
    if cls:
        api.add_resource(cls, *url[:-1])
    # except Exception, e:
    #     print 'Load module error: ', e.message
