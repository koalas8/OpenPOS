
-----------------------------------
------  添加基本数据到数据库 ------
-----------------------------------

-- 添加根用户
INSERT INTO unit_info (unit_no, unit_name, status, remark, weixin_token) VALUES ('00000000', '数据平台', '0', '', '');
INSERT INTO user_info (user_no, real_name, is_admin, unit_no, shop_no, user_level, password, status, address) VALUES ('root', '超级管理员', TRUE, '00000000', NULL, 'super', '670b14728ad9902aecba32e22fa4f6bd', '0', '');
INSERT INTO user_info (user_no, real_name, is_admin, unit_no, shop_no, user_level, password, status, address) VALUES ('sys', '系统用户', TRUE, '00000000', NULL, 'super', '670b14728ad9902aecba32e22fa4f6bd', '1', '');

-- 添加后台功能分类及编号
-- 系统后台功能分类
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('001', '系统权限管理');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('002', '系统操作员管理');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('003', '收银员管理');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('004', '集团管理');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('005', '商户管理');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('006', '终端管理');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('007', '集团互通管理');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('008', '卡管理');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('009', '报表查询');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('010', '会员管理');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('011', '商品管理');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('012', '供应商管理');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('013', '仓库管理');
INSERT INTO "public"."sys_operation_type" (type_code, type_name) VALUES ('014', '营销');

-- 系统权限部分的权限(001**)
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00100', '001', '添加系统权限', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00101', '001', '修改系统权限', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00102', '001', '系统权限列表', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00103', '001', '授权', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00104', '001', '授权修改', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00105', '001', '授权列表', 't', 't', 'f', 'f');
-- 系统操作员部分的权限(002**)                                            
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00200', '002', '添加系统操作员', 't', 't', 'f', 'f');
-- INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00201', '删除/反删除系统操作员', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00202', '002', '修改系统操作员', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00203', '002', '系统操作员列表', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00204', '002', '重置操作员密码', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00206', '002', '赋予操作员权限', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00208', '002', '操作员修改密码', 't', 't', 'f', 'f');
-- POS操作员部分的权限（003**）                                           
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00300', '003', '添加POS操作员', 'f', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00301', '003', '修改POS操作员', 'f', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00303', '003', '查询POS操作员', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00304', '003', '重置POS操作员密码', 'f', 't', 'f', 'f');
-- 集团档案部分的权限（004**）                                            
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00400', '004', '添加集团档案', 't', 'f', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00401', '004', '修改集团档案', 't', 'f', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00402', '004', '集团档案列表', 't', 'f', 'f', 'f');
-- 商户档案部分的权限（005**）                                            
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00500', '005', '添加商户档案', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00501', '005', '修改商户档案', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00502', '005', '商户档案列表', 't', 't', 'f', 'f');
-- 终端档案部分的权限（006**）                                            
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00600', '006', '添加终端档案', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00601', '006', '修改终端档案', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00602', '006', '终端档案列表', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00603', '006', '设置终端权限', 't', 't', 'f', 'f');
-- 集团互通档案部分的权限（007**）                                        
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00700', '007', '添加集团互通', 't', 'f', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00701', '007', '修改集团互通', 't', 'f', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00702', '007', '集团互通列表', 't', 't', 'f', 'f');
-- 卡管理部分的权限（008**）                                            
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00800', '008', '卡信息查询', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00801', '008', '设置卡状态', 'f', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00802', '008', '卡交易流水查询', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00803', '008', '交易监控', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00804', '008', '添加卡分组', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00805', '008', '修改卡分组', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00806', '008', '查看卡分组', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00807', '008', '删除/反删除卡分组', 't', 't', 'f', 'f');
-- 报表部分的权限（009**）                                              
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00900', '009', '账户余额表', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00901', '009', '集团交易统计表', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00902', '009', '商户交易统计表', 't', 't', 't', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00903', '009', '终端交易统计表', 't', 't', 't', 't');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00904', '009', '集团交易明细表', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00905', '009', '商户交易明细表', 't', 't', 't', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00906', '009', '终端交易明细表', 't', 't', 't', 't');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00907', '009', '交易订单表', 't', 't', 't', 't');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('00908', '009', '订单明细表', 't', 't', 't', 't');                     
-- 会员部分权限 (010**)                                                 
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01000', '010', '新会员登记', 'f', 'f', 'f', 't');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01001', '010', '会员列表', 't', 't', 't', 't');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01002', '010', '设置会员等级', 'f', 't', 'f', 'f');                          
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01003', '010', '会员持卡查询', 't', 't', 't', 't');
-- 商品管理部分(011**)                                                  
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01100', '011', '添加新商品', 'f', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01101', '011', '修改商品', 'f', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01102', '011', '查看商品', 'f', 't', 't', 't');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01103', '011', '商品入库', 'f', 't', 't', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01104', '011', '商品销售', 'f', 't', 't', 't');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01105', '011', '查询销售单', 'f', 't', 't', 't');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01106', '011', '查询入库单', 'f', 't', 't', 't');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01107', '011', 'Web POS交易', 'f', 't', 't', 't');
-- INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01108', '011', '采购管理', 'f', 't', 't', 'f');
-- 供应商管理部分(012**)
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01200', '012', '添加新供应商', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01201', '012', '修改供应商', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01202', '012', '查看供应商', 't', 't', 'f', 'f');
-- 仓库管理部分(013**)
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01300', '013', '添加仓库', 'f', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01301', '013', '修改仓库', 'f', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01302', '013', '仓库列表', 'f', 't', 'f', 'f');

-- 营销部分(014**)
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01401', '014', '添加短信模板', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01402', '014', '修改短信模板', 't', 't', 'f', 'f');
INSERT INTO "public"."sys_operation_dim" (operation_code, operation_type_code, operation_name, root_level, unit_level, shop_level, operator_level) VALUES ('01403', '014', '查询短信模板', 't', 't', 'f', 'f');


-- 添加POS功能编号
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000000', '签到');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000010', '消费');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000090', '余额查询');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000060', '积分消费撤销');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000110', '卡启用');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000020', '消费撤销');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000130', '补磁');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000150', '卡改有效期');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000120', '换卡');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000100', '积分查询');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000140', '卡改密码');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000050', '积分消费');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000030', '充值');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000080', '积分充值撤销');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000040', '充值撤销');
INSERT INTO "public"."terminal_trans_dim" (trans_code, trans_name) VALUES ('000070', '积分充值');

-- 添加POS返回码
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('0', '交易成功');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('2', '无效商户');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('3', '无效终端');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('4', '挂失卡');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('5', '冻结卡');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('6', '作废卡');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('7', '过期卡');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('8', '非本系统卡');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('9', '非本集团卡');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('10', '无效卡号');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('11', '新卡未启用');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('12', '卡已启用');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('13', '未知错误');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('14', '密码错');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('15', '数据库错误');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('16', '无效金额');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('17', '余额不足');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('18', '交易记录未找到');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('19', '无效积分');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('20', '积分不足');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('21', '交易已撤销');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('22', '原交易不允许撤销');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('23', '非法卡');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('24', '批次号错');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('25', '流水号错');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('26', 'POS操作员不存在');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('27', 'POS操作员密码错');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('28', 'POS操作员已冻结');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('29', '账不平');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('30', '该卡无此功能');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('31', '终端无此权限');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('32', '无效金额格式');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('33', '无效日期格式');
INSERT INTO "public"."terminal_retcode_dim" (result_code, result_message) VALUES ('61', '该卡已绑定会员');

-- 为 ROOT 用户赋予所有权限
INSERT INTO "public"."role_info" (role_no, role_name, creator, create_datetime, remark, status, unit_no) VALUES ('fef07c7f-f9f7-45d8-84e1-a16cf335a588', '所有权限', 'root', now(), '', '0', '00000000');
INSERT INTO "public"."role_operation" (id, role_no, operation_code) (SELECT uuid_generate_v1(), 'fef07c7f-f9f7-45d8-84e1-a16cf335a588', operation_code FROM sys_operation_dim WHERE root_level = 't');
UPDATE "public"."user_info" SET role_no = 'fef07c7f-f9f7-45d8-84e1-a16cf335a588' WHERE user_no in ('root', 'sys');
