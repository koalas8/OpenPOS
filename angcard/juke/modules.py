# coding: utf-8
from sqlalchemy import Table, MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from juke import app as _app

engine = create_engine(_app.config['DATABASE_URI'], echo=_app.config['DATABASE_ECHO'])
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

@_app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

Base = declarative_base()
metadata = MetaData(bind=engine)

Base.query = db_session.query_property()

class UnitInfo(Base):
    __table__ = Table('unit_info', metadata, autoload=True)


class InterInfo(Base):
    __table__ = Table('inter_info', metadata, autoload=True)


class ShopInfo(Base):
    __table__ = Table('shop_info', metadata, autoload=True)


class TerminalRetcodeDim(Base):
    __table__ = Table('terminal_retcode_dim', metadata, autoload=True)


class SysOperationType(Base):
    __table__ = Table('sys_operation_type', metadata, autoload=True)


class SysOperationDim(Base):
    __table__ = Table('sys_operation_dim', metadata, autoload=True)


class RoleInfo(Base):
    __table__ = Table('role_info', metadata, autoload=True)


class RoleOperation(Base):
    __table__ = Table('role_operation', metadata, autoload=True)


class UserInfo(Base):
    __table__ = Table('user_info', metadata, autoload=True)


class TerminalInfo(Base):
    __table__ = Table('terminal_info', metadata, autoload=True)


class UnitManager(Base):
    __table__ = Table('unit_manager', metadata, autoload=True)


class PointsRule(Base):
    __table__ = Table('points_rule', metadata, autoload=True)


class TerminalTransDim(Base):
    __table__ = Table('terminal_trans_dim', metadata, autoload=True)


class TerminalTransInfo(Base):
    __table__ = Table('terminal_trans', metadata, autoload=True)


class CardBatchInfo(Base):
    __table__ = Table('card_batch_info', metadata, autoload=True)


class CardResource(UnitInfo):
    __table__ = Table('card_resource', metadata, autoload=True)


class TmpCardInfo(Base):
    __table__ = Table('tmp_card_info', metadata, autoload=True)


class CardGroupInfo(Base):
    __table__ = Table('card_group', metadata, autoload=True)


class CardLevelInfo(Base):
    __table__ = Table('card_level_info', metadata, autoload=True)


class CardInfo(Base):
    __table__ = Table('card_info', metadata, autoload=True)


class Trans(Base):
    __table__ = Table('trans', metadata, autoload=True)


class Gift(Base):
    __table__ = Table('gift', metadata, autoload=True)


class SysCityDim(Base):
    __table__ = Table('sys_city_dim', metadata, autoload=True)


class MemberInfo(Base):
    __table__ = Table('member', metadata, autoload=True)


class SupplierInfo(Base):
    __table__ = Table('supplier', metadata, autoload=True)


class WarehouseInfo(Base):
    __table__ = Table('warehouse', metadata, autoload=True)


class SizeGroupInfo(Base):
    __table__ = Table('size_group', metadata, autoload=True)


class SizeGroupDetail(Base):
    __table__ = Table('size_group_detail', metadata, autoload=True)


class GoodsClassInfo(Base):
    __table__ = Table('goods_class_info', metadata, autoload=True)


class GoodsBaseInfo(Base):
    __table__ = Table('goods_base_info', metadata, autoload=True)


class GoodsPurchaseOrderInfo(Base):
    __table__ = Table('purchase_order', metadata, autoload=True)


class GoodsInfo(Base):
    __table__ = Table('goods_info', metadata, autoload=True)


class SaleOrderInfo(Base):
    __table__ = Table('sale_order', metadata, autoload=True)


class SaleOrderDetail(Base):
    __table__ = Table('sale_order_detail', metadata, autoload=True)


class WarehouseReceiptInfo(Base):
    __table__ = Table('warehouse_receipt', metadata, autoload=True)


class SMSTemplate(Base):
    __table__ = Table('sms_template', metadata, autoload=True)


class SMSListInfo(Base):
    __table__ = Table('sms_list', metadata, autoload=True)


# class FeedbackInfo(Base):
#     __table__ = Table('feedback', metadata, autoload=True)

# class Settings(Base):
#     __table__ = Table('settings', metadata, autoload=True)

# class WeChatTemplate(Base):
#     __table__ = Table('wechat_msg_template', metadata, autoload=True)