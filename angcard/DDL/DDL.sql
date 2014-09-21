CREATE TABLE sys_operation_type (
    type_code VARCHAR(3) NOT NULL,
    type_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (type_code)
);


CREATE TABLE sys_operation_dim (
    operation_code VARCHAR(6) NOT NULL,
    operation_type_code VARCHAR(3) NOT NULL,
    operation_name VARCHAR(100) NOT NULL,
    unit_level BOOLEAN DEFAULT 'f' NOT NULL,  -- 是否是集团级用户
    shop_level BOOLEAN DEFAULT 'f' NOT NULL,  -- 是否是商户级用户
    root_level BOOLEAN DEFAULT 'f' NOT NULL,  -- 是否是终端级用户
    operator_level BOOLEAN DEFAULT 'f' NOT NULL,
    PRIMARY KEY (operation_code),
    FOREIGN KEY (operation_type_code) REFERENCES sys_operation_type(type_code)
);


CREATE TABLE unit_info (
    unit_no VARCHAR(8) NOT NULL,
    unit_name VARCHAR(100) NOT NULL,
    create_datetime TIMESTAMP NOT NULL DEFAULT 'now()',  -- 创建时间
    type VARCHAR(1) NOT NULL DEFAULT '0',  -- 账户类型：0免费账户 1一级账户 2二级账户...(值越高，级别越高)
    shop_limit INTEGER NOT NULL DEFAULT 1,  -- 可创建商户数
    status VARCHAR(1) DEFAULT '0' NOT NULL,
    weixin_token VARCHAR(255) DEFAULT '' NOT NULL,
    remark TEXT DEFAULT '' NOT NULL,
    sms_amount INTEGER NOT NULL DEFAULT 0,  -- 拥有短信的条数
    sms_send INTEGER NOT NULL DEFAULT 0,  -- 已发送条数
    PRIMARY KEY (unit_no)
);


CREATE TABLE sys_city_dim (
    id SERIAL NOT NULL,
    city VARCHAR(255) NOT NULL,
    level INTEGER NOT NULL,
    pid INTEGER,
    PRIMARY KEY (id)
);


CREATE TABLE terminal_trans_dim (
    trans_code VARCHAR(6) NOT NULL,
    trans_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (trans_code)
);


CREATE TABLE terminal_retcode_dim (
    result_code VARCHAR(2) NOT NULL,
    result_message VARCHAR(100) NOT NULL,
    PRIMARY KEY (result_code)
);


CREATE TABLE shop_info (
    shop_no VARCHAR(15) NOT NULL,
    shop_type VARCHAR (1) NOT NULL DEFAULT '0',  -- 0通用系统 1服装系统 2美容美发
    address VARCHAR(200) DEFAULT '' NOT NULL,
    points_rule INTEGER DEFAULT '0' NOT NULL,
    create_datetime TIMESTAMP NOT NULL DEFAULT 'now()',
    remark TEXT DEFAULT '' NOT NULL,
    shop_name VARCHAR(100) NOT NULL,
    status VARCHAR(1) DEFAULT '0' NOT NULL,
    unit_no VARCHAR(8) NOT NULL,
    sys_type VARCHAR (1) NOT NULL DEFAULT '0',  -- 0通用系统 1鞋服系统
    PRIMARY KEY (shop_no),
    FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE card_batch_info (
    id UUID NOT NULL default uuid_generate_v4(),
    batch_no INTEGER NOT NULL,
    file_generated BOOLEAN NOT NULL,
    remark TEXT DEFAULT '' NOT NULL,
    unit_no VARCHAR(8) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE gift (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    gift_name VARCHAR(255) NOT NULL,
    points INTEGER DEFAULT '0' NOT NULL,
    status VARCHAR(1) DEFAULT '0' NOT NULL,
    unit_no VARCHAR(8) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE role_info (
    role_no UUID NOT NULL,
    role_name VARCHAR(100) NOT NULL,
    create_datetime TIMESTAMP WITHOUT TIME ZONE DEFAULT 'now()' NOT NULL,
    creator VARCHAR(100) NOT NULL,
    remark TEXT DEFAULT '' NOT NULL,
    status VARCHAR(1) DEFAULT '0' NOT NULL,
    unit_no VARCHAR(8) NOT NULL,
    PRIMARY KEY (role_no),
    FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE card_resource (
    unit_no VARCHAR(8) NOT NULL,
    start_batch_no INTEGER NOT NULL,
    start_card_no INTEGER NOT NULL,
    PRIMARY KEY (unit_no),
    FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE tmp_card_info (
    card_no VARCHAR(19) NOT NULL,
    amount INTEGER NOT NULL,
    times INTEGER NOT NULL DEFAULT 0,
    batch_no INTEGER NOT NULL,
    card_kind VARCHAR(1) DEFAULT '0',  -- 卡类型：充值卡/定额卡/计次卡/计时卡
    card_type VARCHAR(1) DEFAULT '0' NOT NULL,  -- 卡来源：0系统卡/1客户原有的自发卡
    exp_date VARCHAR(8) DEFAULT '',
    password VARCHAR(255) NOT NULL,
    points INTEGER DEFAULT '0' NOT NULL,
    points_rule FLOAT DEFAULT '0.00' NOT NULL,
    recharge_flag BOOLEAN NOT NULL,
    pre_status VARCHAR(1) DEFAULT '' NOT NULL,
    status VARCHAR(1) DEFAULT '0' NOT NULL,
    track_2 VARCHAR(37) NOT NULL,
    unit_no VARCHAR(8) NOT NULL,
    valid_life INTEGER DEFAULT '6' NOT NULL,
    property_deposit BOOLEAN NOT NULL DEFAULT 't',
    property_times BOOLEAN NOT NULL DEFAULT 'f',
    PRIMARY KEY (card_no),
    FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE inter_info (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    credit_unit VARCHAR(8) NOT NULL,
    debit_unit VARCHAR(8) NOT NULL,
    remark TEXT DEFAULT '' NOT NULL,
    status VARCHAR(1) DEFAULT '0' NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(credit_unit) REFERENCES unit_info (unit_no),
    FOREIGN KEY(debit_unit) REFERENCES unit_info (unit_no)
);


CREATE TABLE member (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    address VARCHAR(200) DEFAULT '' NOT NULL,
    birthday VARCHAR(8) DEFAULT '' NOT NULL,
    province INTEGER,
    city INTEGER,
    country INTEGER,
    district INTEGER,
    email VARCHAR(255) DEFAULT '' NOT NULL,
    idcard VARCHAR(18) DEFAULT '' NOT NULL,
    member_name VARCHAR(20) NOT NULL,
    name_initials VARCHAR(10) NOT NULL DEFAULT '',
    name_pinyin VARCHAR(100) NOT NULL DEFAULT '',
    phone VARCHAR(11) NOT NULL DEFAULT '',
    last_trans_time TIMESTAMP NOT NULL DEFAULT 'now()',  -- 最近一次的交易时间
    register_datetime TIMESTAMP WITHOUT TIME ZONE DEFAULT 'now()' NOT NULL,
    sex CHARACTER VARYING(1) DEFAULT 'F' NOT NULL,
    shop_no CHARACTER VARYING(15) NOT NULL,
    unit_no CHARACTER VARYING(8) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(province) REFERENCES sys_city_dim (id),
    FOREIGN KEY(city) REFERENCES sys_city_dim (id),
    FOREIGN KEY(country) REFERENCES sys_city_dim (id),
    FOREIGN KEY(district) REFERENCES sys_city_dim (id),
    FOREIGN KEY(shop_no) REFERENCES shop_info (shop_no),
    FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE user_info (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    user_no CHARACTER VARYING(100) NOT NULL,
    address CHARACTER VARYING(200) DEFAULT '' NOT NULL,
    is_admin BOOLEAN DEFAULT 'f' NOT NULL,
    password CHARACTER VARYING(32) DEFAULT '670b14728ad9902aecba32e22fa4f6bd' NOT NULL,
    real_name CHARACTER VARYING(100) DEFAULT '' NOT NULL,
    email CHARACTER VARYING (100) DEFAULT '' NOT NULL,
    reg_time TIMESTAMP NOT NULL DEFAULT 'now',
    role_no UUID,
    unit_no CHARACTER VARYING(8),
    shop_no CHARACTER VARYING(15),
    status CHARACTER VARYING(1) DEFAULT '0' NOT NULL,  -- 0正常 1冻结 2预注册
    user_level CHARACTER VARYING(10) DEFAULT 'shop' NOT NULL,
    token UUID NOT NULL DEFAULT uuid_generate_v4(),  -- 用户令牌，注册时用
    api CHARACTER VARYING (1) NOT NULL DEFAULT '0',  -- 0不是weibo用户 1新浪weibo 2腾讯weibo 3QQ号
    -- ****** 新浪微博 ******
    sina_weibo_uid CHARACTER VARYING (10) NOT NULL DEFAULT '',  -- 新浪微博账号
    sina_weibo_profile_image CHARACTER VARYING (36) NOT NULL DEFAULT '',  -- 新浪微博头像
    sina_weibo_screen_name CHARACTER VARYING (100) NOT NULL DEFAULT '',  -- 新浪微博昵称
    sina_weibo_token CHARACTER VARYING (32) NOT NULL DEFAULT '',  -- 新浪微博TOKEN
    PRIMARY KEY (user_no),
    FOREIGN KEY(role_no) REFERENCES role_info (role_no),
    FOREIGN KEY(shop_no) REFERENCES shop_info (shop_no),
    FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE role_operation (
    id UUID NOT NULL default uuid_generate_v4(),
    operation_code CHARACTER VARYING(6) NOT NULL,
    role_no UUID NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(operation_code) REFERENCES sys_operation_dim (operation_code),
    FOREIGN KEY(role_no) REFERENCES role_info (role_no)
);


CREATE TABLE card_group (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    create_datetime TIMESTAMP WITHOUT TIME ZONE DEFAULT 'now()' NOT NULL,
    creator CHARACTER VARYING(100) NOT NULL,
    group_name CHARACTER VARYING(255) NOT NULL,
    status CHARACTER VARYING(1) DEFAULT '0' NOT NULL,
    unit_no CHARACTER VARYING(8) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(creator) REFERENCES user_info (user_no),
    FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no)
);


CREATE TABLE unit_manager (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    remark TEXT DEFAULT '' NOT NULL,

    unit_no CHARACTER VARYING(8) NOT NULL,
    user_no CHARACTER VARYING(20) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(unit_no) REFERENCES unit_info (unit_no),
    FOREIGN KEY(user_no) REFERENCES user_info (user_no)
);


CREATE TABLE terminal_info (
    terminal_no CHARACTER VARYING(8) NOT NULL,
    batch_no INTEGER DEFAULT '1' NOT NULL,
    current_operator CHARACTER VARYING(20),
    des_key CHARACTER VARYING(36),
    is_default BOOLEAN DEFAULT 'f' NOT NULL,
    create_datetime TIMESTAMP NOT NULL DEFAULT 'now()',
    remark TEXT DEFAULT '' NOT NULL,
    shop_no CHARACTER VARYING(15) NOT NULL,
    status CHARACTER VARYING(1) DEFAULT '0' NOT NULL,
    trace_no INTEGER DEFAULT '1' NOT NULL,
    PRIMARY KEY (terminal_no),
    FOREIGN KEY(current_operator) REFERENCES user_info (user_no),
    FOREIGN KEY(shop_no) REFERENCES shop_info (shop_no)
);


CREATE TABLE points_rule (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    create_time TIMESTAMP WITHOUT TIME ZONE DEFAULT 'now()' NOT NULL,
    creator CHARACTER VARYING(100) NOT NULL,
    credit_unit CHARACTER VARYING(8) NOT NULL,
    debit_unit CHARACTER VARYING(8) NOT NULL,
    points_rule INTEGER DEFAULT '0' NOT NULL,
    statue CHARACTER VARYING(1) DEFAULT '0' NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(creator) REFERENCES user_info (user_no),
    FOREIGN KEY(credit_unit) REFERENCES unit_info (unit_no),
    FOREIGN KEY(debit_unit) REFERENCES unit_info (unit_no)
);


CREATE TABLE terminal_trans (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    terminal_no CHARACTER VARYING(8) NOT NULL,
    trans_code CHARACTER VARYING(6) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(terminal_no) REFERENCES terminal_info (terminal_no),
    FOREIGN KEY(trans_code) REFERENCES terminal_trans_dim (trans_code)
);


CREATE TABLE card_level_info (
    cl_id UUID NOT NULL,
    cl_unit_no CHAR(8) NOT NULL,
    cl_level_name CHARACTER VARYING(50) NOT NULL,
    PRIMARY KEY (cl_id),
    FOREIGN KEY (cl_unit_no) REFERENCES unit_info (unit_no)
);

-- 卡状态：0新卡未启用 1正常卡 2挂失卡 3 冻结卡 4作废卡
CREATE TABLE card_info (
    card_no CHARACTER VARYING(19) NOT NULL,
    custom_card_no CHARACTER VARYING(19) NOT NULL DEFAULT '',   -- 用户自有卡的卡号，自有卡不能与系统卡共用card_no字雄，因为card_no字雄是不允许重复的，但自有卡在不同的集团是允许有重复的
    property_deposit BOOLEAN NOT NULL DEFAULT 't',  -- 能否充值
    property_times BOOLEAN NOT NULL DEFAULT 'f',  -- 是否是次卡
    amount INTEGER NOT NULL,  -- 卡内余额，以分计
    times INTEGER NOT NULL DEFAULT 0,  -- 还有几次
    card_kind CHARACTER VARYING(1) DEFAULT '0' NOT NULL, -- 卡类型 0：磁条卡 1：IC接解卡 2：IC非接触
    card_type CHARACTER VARYING(1) NOT NULL,  -- 卡种类：0系统卡 1自发卡
    card_group UUID,
    member_id UUID,
    exp_date CHARACTER VARYING(8) DEFAULT '' NOT NULL,  -- 过期日期
    password CHARACTER VARYING(32) NOT NULL,
    points INTEGER DEFAULT '0' NOT NULL,
    points_rule FLOAT DEFAULT '0.00' NOT NULL,
    pre_status CHARACTER VARYING(1) DEFAULT '' NOT NULL,
    status CHARACTER VARYING(1) DEFAULT '0' NOT NULL,
    total_pay INTEGER DEFAULT '0' NOT NULL,
    track_2 CHARACTER VARYING(37) NOT NULL,
    unit_no CHARACTER VARYING(8) NOT NULL,
    valid_life INTEGER NOT NULL,
    card_level_id UUID,
    last_trans_time TIMESTAMP NOT NULL DEFAULT 'now()',
    PRIMARY KEY (card_no),
    FOREIGN KEY (card_group) REFERENCES card_group (id),
    FOREIGN KEY (unit_no) REFERENCES unit_info (unit_no),
    FOREIGN KEY (card_level_id) REFERENCES card_level_info (cl_id)
);


CREATE TABLE trans (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    amount INTEGER NOT NULL,
    amount_balance INTEGER NOT NULL,
    award_amount INTEGER DEFAULT '0' NOT NULL,
    award_points INTEGER DEFAULT '0' NOT NULL,
    batch_no INTEGER NOT NULL,
    card_no CHARACTER VARYING(19) NOT NULL,
    credit_unit CHARACTER VARYING(8) NOT NULL,
    reversiable CHARACTER VARYING(1) DEFAULT '0' NOT NULL,
    debit_unit CHARACTER VARYING(8) NOT NULL,
    interface CHARACTER VARYING(1) DEFAULT '0' NOT NULL,
    points INTEGER DEFAULT '0' NOT NULL,
    points_balance INTEGER NOT NULL,
    points_rule FLOAT DEFAULT '0.00' NOT NULL,
    pos_operator CHARACTER VARYING(20),
    result_code CHARACTER VARYING(2) NOT NULL,
    shop_no CHARACTER VARYING(15) NOT NULL,
    terminal_no CHARACTER VARYING(8) NOT NULL,
    trace_no INTEGER NOT NULL,
    trans_code CHARACTER VARYING(6) NOT NULL,
    trans_date CHARACTER VARYING(8) NOT NULL,
    trans_time CHARACTER VARYING(6) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(card_no) REFERENCES card_info (card_no),
    FOREIGN KEY(credit_unit) REFERENCES unit_info (unit_no),
    FOREIGN KEY(debit_unit) REFERENCES unit_info (unit_no),
    FOREIGN KEY(pos_operator) REFERENCES user_info (user_no),
    FOREIGN KEY(result_code) REFERENCES terminal_retcode_dim (result_code),
    FOREIGN KEY(shop_no) REFERENCES shop_info (shop_no),
    FOREIGN KEY(terminal_no) REFERENCES terminal_info (terminal_no),
    FOREIGN KEY(trans_code) REFERENCES terminal_trans_dim (trans_code)
);


-- CREATE TABLE history_trans (
--  id UUID NOT NULL DEFAULT uuid_generate_v4(),
--  amount INTEGER NOT NULL,
--  amount_balance INTEGER NOT NULL,
--  award_amount INTEGER DEFAULT '0' NOT NULL,
--  award_points INTEGER DEFAULT '0' NOT NULL,
--  batch_no INTEGER NOT NULL,
--  card_no CHARACTER VARYING(19) NOT NULL,
--  credit_unit CHARACTER VARYING(8) NOT NULL,
--  reversiable CHARACTER VARYING(1) DEFAULT '0' NOT NULL,  -- 0原交易可撤销 1原交易已撤销，不能再次撤销 2原交易不支持撤销
--  debit_unit CHARACTER VARYING(8) NOT NULL,
--  interface CHARACTER VARYING(1) DEFAULT '0' NOT NULL,
--  points INTEGER DEFAULT '0' NOT NULL,
--  points_balance INTEGER NOT NULL,
--  points_rule FLOAT DEFAULT '0.00' NOT NULL,
--  pos_operator CHARACTER VARYING(20),
--  result_code CHARACTER VARYING(2) NOT NULL,
--  shop_no CHARACTER VARYING(15) NOT NULL,
--  terminal_no CHARACTER VARYING(8) NOT NULL,
--  trace_no INTEGER NOT NULL,
--  trans_code CHARACTER VARYING(6) NOT NULL,
--  trans_date CHARACTER VARYING(8) NOT NULL,
--  trans_time CHARACTER VARYING(6) NOT NULL,
--  PRIMARY KEY (id),
--  FOREIGN KEY(card_no) REFERENCES card_info (card_no),
--  FOREIGN KEY(credit_unit) REFERENCES unit_info (unit_no),
--  FOREIGN KEY(debit_unit) REFERENCES unit_info (unit_no),
--  FOREIGN KEY(pos_operator) REFERENCES user_info (user_no),
--  FOREIGN KEY(shop_no) REFERENCES shop_info (shop_no),
--  FOREIGN KEY(terminal_no) REFERENCES terminal_info (terminal_no),
--  FOREIGN KEY(trans_code) REFERENCES terminal_trans_dim (trans_code)
-- );


CREATE TABLE supplier
(
    id uuid default uuid_generate_v4() NOT NULL,
    supplier_name CHARACTER VARYING(100),
    contect CHARACTER VARYING(10) DEFAULT '' NOT NULL,
    tel CHARACTER VARYING(12) DEFAULT '' NOT NULL,
    email CHARACTER VARYING(50) DEFAULT '' NOT NULL,
    unit_no CHARACTER VARYING(8) NOT NULL,
    address CHARACTER VARYING(100) NOT NULL DEFAULT '',
    status CHARACTER VARYING(1) NOT NULL DEFAULT '0',
    PRIMARY KEY(id),
    FOREIGN KEY (unit_no) REFERENCES unit_info(unit_no)
);


-- 仓库信息
CREATE TABLE warehouse
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    warehouse_name CHARACTER VARYING(50) NOT NULL,
    status CHARACTER VARYING(1) NOT NULL DEFAULT '0',
    unit_no CHARACTER VARYING(8) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (unit_no) REFERENCES unit_info (unit_no)
);


-- 品牌
-- CREATE TABLE brand_info (
--  id UUID NOT NULL DEFAULT uuid_generate_v4(),
--  unit_no CHARACTER VARYING(8) NOT NULL,
--  shop_no CHARACTER VARYING(15),
--  brand_name CHARACTER VARYING(20) NOT NULL,
--  PRIMARY KEY (id),
--  FOREIGN KEY (unit_no) REFERENCES unit_info (unit_no),
--  FOREIGN KEY (shop_no) REFERENCES shop_info (shop_no)
-- );


-- 尺寸分组表
CREATE TABLE size_group (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    group_name CHARACTER VARYING(100) NOT NULL,
    unit_no CHARACTER VARYING(8) NOT NULL,
    shop_no CHARACTER VARYING(15),
    PRIMARY KEY (id),
    FOREIGN KEY (unit_no) REFERENCES unit_info (unit_no),
    FOREIGN KEY (shop_no) REFERENCES shop_info (shop_no)
);

-- 尺寸组明细
CREATE TABLE size_group_detail (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    group_id UUID NOT NULL,
    size CHARACTER VARYING(10) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (group_id) REFERENCES size_group (id)
);


-- 商品类别信息
CREATE TABLE goods_class_info
(
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  pid uuid,
  size_group_id UUID,
  class_name CHARACTER VARYING (50) NOT NULL DEFAULT '',
  unit_no CHARACTER VARYING (8) NOT NULL,
  shop_no CHARACTER VARYING (15),
  status CHARACTER VARYING (1) NOT NULL DEFAULT '0',
  PRIMARY KEY (id),
  FOREIGN KEY (unit_no) REFERENCES unit_info (unit_no),
  FOREIGN KEY (shop_no) REFERENCES shop_info (shop_no)
);

-- 商品基本信息
CREATE TABLE goods_base_info (
  id UUID NOT NULL DEFAULT uuid_generate_v4(),
  class_id UUID,
  goods_name CHARACTER VARYING (100) NOT NULL,
  barcode CHARACTER VARYING (13),  -- 商品条码
  unit_no CHARACTER VARYING (8) NOT NULL,
  shop_no CHARACTER VARYING (15),
  supplier_id UUID,  -- 供应商ID
  status CHARACTER VARYING (1) NOT NULL DEFAULT '0',
  PRIMARY KEY (id),
  FOREIGN KEY (class_id) REFERENCES goods_class_info(id),
  FOREIGN KEY (unit_no) REFERENCES unit_info(unit_no)
);


-- 采购单
CREATE TABLE purchase_order (
  id UUID NOT NULL DEFAULT uuid_generate_v4(),
  creator CHARACTER VARYING (100) NOT NULL,
  create_datetime TIMESTAMP NOT NULL DEFAULT 'now()',
  goods_amount INTEGER NOT NULL DEFAULT 0,
  cash_amount INTEGER NOT NULL DEFAULT 0,
  unit_no CHARACTER VARYING (8) NOT NULL,
  shop_no CHARACTER VARYING (15) NOT NULL DEFAULT '',
  PRIMARY KEY (id),
  FOREIGN KEY (creator) REFERENCES user_info (user_no),
  FOREIGN KEY (unit_no) REFERENCES unit_info (unit_no)
);

-- 商品信息
CREATE TABLE goods_info
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    goods_id UUID NOT NULL,  -- goods_base_info -> id
    goods_name CHARACTER VARYING (100) NOT NULL DEFAULT '',  -- 商品名称，采购时用户可自行修改
    purchase_order_id UUID,
    color CHARACTER VARYING (7) NOT NULL DEFAULT '',  -- 颜色，鞋服类商品需要
    size CHARACTER VARYING (10) NOT NULL DEFAULT '',  -- 大小/型号， 鞋服类需要
    goods_amount INTEGER NOT NULL DEFAULT 0,  -- 商品总数
    purchase_price INTEGER NOT NULL DEFAULT 0,  -- 进货价
    label_price INTEGER NOT NULL DEFAULT 0,  -- 标签价
    sale_price INTEGER NOT NULL DEFAULT 0,  -- 售价
    pack_unit CHARACTER VARYING(10) NOT NULL DEFAULT '',
    status CHARACTER VARYING(1) NOT NULL DEFAULT '0',
    pinyin CHARACTER VARYING(300) NOT NULL DEFAULT '',
    pinyin_initial CHARACTER(100) NOT NULL DEFAULT '',
    brief_code CHARACTER VARYING(10) NOT NULL DEFAULT '',
    unit_no CHARACTER VARYING (8) NOT NULL,
    shop_no CHARACTER VARYING (15) NOT NULL DEFAULT '',
    PRIMARY KEY (id),
    FOREIGN KEY (goods_id) REFERENCES goods_base_info(id),
    FOREIGN KEY (unit_no) REFERENCES unit_info(unit_no)
);

-- 进销存销售订单
CREATE TABLE sale_order
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),  -- 同为订单号
    create_time TIMESTAMP(6)  NOT NULL DEFAULT 'now()',  -- 订单创建时间
    pay_time TIMESTAMP(6) DEFAULT NULL,  -- 订单支付时间
    goods_amount INTEGER NOT NULL DEFAULT 0,  -- 此订单物品数量
    amount INTEGER NOT NULL DEFAULT 0,  -- 订单总额，以分为单位
    is_paid BOOLEAN NOT NULL DEFAULT 'f',  -- 是否已付款
    profit INTEGER NOT NULL DEFAULT 0,  -- 此单利润
    user_no CHARACTER VARYING(100) NOT NULL DEFAULT '',
    unit_no CHARACTER VARYING(8) NOT NULL,
    mode_of_payment CHARACTER VARYING(6) NOT NULL DEFAULT 'card',  -- 支付方式: card, cash, point, mixed
    card_pay_amount INTEGER NOT NULL DEFAULT 0,
    cash_pay_amount INTEGER NOT NULL DEFAULT 0,
    point_pay_amount INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    FOREIGN KEY (user_no) REFERENCES user_info(user_no),
    FOREIGN KEY (unit_no) REFERENCES unit_info(unit_no)
);


-- 订单明细表
CREATE TABLE sale_order_detail (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    order_id uuid NOT NULL,
    goods_id uuid NOT NULL,
    goods_amount INTEGER NOT NULL DEFAULT 0,  -- 此单此种商品数量
    purchase_price INTEGER NOT NULL DEFAULT 0,  -- 进价
    label_price INTEGER NOT NULL DEFAULT 0,  -- 吊牌价
    sale_price INTEGER NOT NULL DEFAULT 0,  -- 售价
    discount INTEGER NOT NULL DEFAULT 100,  -- 折扣值，计算时需要除以100
    PRIMARY KEY (id),
    FOREIGN KEY (order_id) REFERENCES sale_order(id),
    FOREIGN KEY (goods_id) REFERENCES goods_info(id)
);


-- 入库单信息
CREATE TABLE warehouse_receipt
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    unit_no CHARACTER VARYING(8) NOT NULL,
    goods_id UUID NOT NULL,
    goods_name CHARACTER VARYING(50) NOT NULL,
    purchase_price INTEGER NOT NULL,  -- 进货价
    create_time TIMESTAMP(6) WITHOUT TIME ZONE,
    amount INTEGER NOT NULL,  -- 进货数量
    PRIMARY KEY (id),
    FOREIGN KEY (unit_no) REFERENCES unit_info (unit_no),
    FOREIGN KEY (goods_id) REFERENCES goods_info (id)
);


CREATE TABLE discount
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    card_group UUID NOT NULL,
    shop_no CHARACTER VARYING(15) NOT NULL,
    discount numeric(3, 2) NOT NULL DEFAULT 1.00,
    creator CHARACTER VARYING(100) NOT NULL,
    create_datetime TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL DEFAULT 'now()',
    status CHARACTER VARYING(1) NOT NULL DEFAULT '0',
    PRIMARY KEY(id),
    FOREIGN KEY (card_group) REFERENCES card_group(id),
    FOREIGN KEY (shop_no) REFERENCES shop_info(shop_no),
    FOREIGN KEY (creator) REFERENCES user_info(user_no)
);


CREATE TABLE sms_template (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    template_name CHARACTER VARYING(20) NOT NULL,
    template_content TEXT NOT NULL DEFAULT '',
    template_level CHARACTER VARYING(5) NOT NULL,  -- 短信模板级别：unit/shop
    unit_no CHARACTER VARYING(8) NOT NULL,
    shop_no CHARACTER VARYING(15),
    status CHARACTER VARYING(1) NOT NULL DEFAULT '0',
    PRIMARY KEY (id),
    FOREIGN KEY (unit_no) REFERENCES unit_info (unit_no),
    FOREIGN KEY (shop_no) REFERENCES shop_info(shop_no)
);


CREATE TABLE sms_list (
    id uuid NOT NULl DEFAULT uuid_generate_v4(),
    unit_no CHARACTER VARYING(8) NOT NULL,
    shop_no CHARACTER VARYING(15),
    phone CHARACTER VARYING(11) NOT NULL,
    phone_timestamp CHARACTER VARYING(22) NOT NULL DEFAULT '',
    send_datetime TIMESTAMP NOT NULL default 'now()',
    confirmed_datetime TIMESTAMP,  -- 短信接口提供商返回的送达时间
    content TEXT NOT NULL,
    status CHARACTER VARYING(3) NOT NULL DEFAULT '0',  -- 此状态码参照短信接口返回的状态码
    PRIMARY KEY (id),
    FOREIGN KEY (unit_no) REFERENCES unit_info (unit_no),
    FOREIGN KEY (shop_no) REFERENCES shop_info (shop_no)
);


CREATE TABLE wechat_msg_template (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    unit_no CHARACTER VARYING(8) NOT NULL,
    shop_no CHARACTER VARYING(15) NOT NULL,
    template_level CHARACTER VARYING(4) NOT NULL,  -- 微信模板级别：unit/shop
    request_msg_type CHARACTER VARYING(5) NOT NULL,
    request_msg_content CHARACTER VARYING(200) NOT NULL,
    response_msg_type CHARACTER VARYING(5) NOT NULL,
    response_msg_content JSON NOT NULL,
    status CHARACTER VARYING(1) NOT NULL DEFAULT '0',
    PRIMARY KEY (id),
    FOREIGN KEY (unit_no) REFERENCES unit_info (unit_no),
    FOREIGN KEY (shop_no) REFERENCES shop_info(shop_no)
);

CREATE TABLE settings (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    unit_no CHARACTER VARYING(8) NOT NULL,
    shop_no CHARACTER VARYING(15) NOT NULL DEFAULT '',
    ticket_head CHARACTER VARYING (100) NOT NULL DEFAULT '-= 购物小票 =-',
    ticket_foot CHARACTER VARYING (100) NOT NULL DEFAULT '-= 感谢您的惠顾 =-'
);


-- 2014.04.25 新增
CREATE TABLE feedback (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    unit_no CHARACTER VARYING(8) NOT NULL,
    shop_no CHARACTER VARYING(15) NOT NULL DEFAULT '',
    creator CHARACTER VARYING(100) NOT NULL,
    create_datetime TIMESTAMP NOT NULL DEFAULT 'now()',
    title CHARACTER VARYING(200) NOT NULL DEFAULT '',
    content TEXT NOT NULL DEFAULT '',
    status CHARACTER VARYING(1) NOT NULL DEFAULT '1',  -- 反馈状态 0:已受理 1:未受理
    PRIMARY KEY (id)
);