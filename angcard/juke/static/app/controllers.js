'use strict';

/* Controllers */
var DEBUG = false;

/* Global parameters */
var g = {'card_bin': '999'}

//console.log(UUID.prototype.createUUID());

angular.module('angcardApp.controllers', [])

	.controller('RootCtrl', ['$scope', '$http', '$localStorage', '$location',
		function($scope, $http, $localStorage, $location) {
			$scope.$storage = $localStorage.$default({
				members: [],
				// 通知中心本地存储格式：notices = [{id:'', title:'', content:'', event:'', ...}]
				notices: []
			});

			$scope.root = function() {
				return {
					menu: function() {
						return {
							show: function(operationCode) {
								if (DEBUG) return true;
								// 读取cookie
								var myOperations = '';
								var arrStr = document.cookie.split(';');
								for (var i = 0; i < arrStr.length; i++) {
									var tmp = arrStr[i].split('=');
									if (tmp[0].trim() == 'operations') {
										myOperations = unescape(tmp[1]).split('-');
										break;
									}
								}
								// console.log(myOperations);
								var operations = operationCode.split('-');
								var showSign = false; // 默认不显示

								if (operations.length == 1) { // 最低级别的子菜单（功能菜单）
									if ($.inArray(operations[0], myOperations) == -1) {
										// console.log(operations[0] + '不在权限列表中');
										showSign = false; // 不显示
									} else {
										showSign = true; // 显示
									}
								} else {
									for (var i = 0; i < operations.length; i++) {
										if ($.inArray(operations[i], myOperations) > -1) {
											showSign = true;
											// console.log(operations + '在权限列表中');
											break;
										}
									}
								}

								return showSign;
							}
						};
					}(),
					notice: function () {
						return {
							set: function (notice) {  // 添加或更新
								var notices = $scope.$storage.notices;
								var myDate = new Date();
								notice.time = myDate.getHours() + ":" + myDate.getMinutes() + ":" + myDate.getSeconds();
								for (var i=0; i<notices.length; i++) {
									if (notices[i].id == notice.id) {
										notices[i] = notice;
										return;
									}
								}
								notices.push(notice);
							},
							get: function(noticeId) {
								var notices = $scope.$storage.notices;
								for (var i=0; i<notices.length; i++) {
									if (notices[i].id == noticeId) {
										return notices[i];
									}
								}
								return null;
							},
							remove: function (id) {
								var notices = $scope.$storage.notices;
								for (var i=0; i<notices.length; i++) {
									if (notices[i].id == id) {
										notices.splice(i, 1);
									}
								}
							},
							count: function () {
								return $scope.$storage.notices.length;
							},
							clear: function () {
								$scope.$storage.notices = [];
							},
							current: null,
							click: function(_noticeId, _event) {
								_event = _event.toLowerCase();
								switch (_event) {
									case 'showSelectedMembers'.toLowerCase():
										var notice = this.get(_noticeId);
										if (notice) {
											this.current = notice;
										} else {
											this.current = {title: '信息', content: '您查询的消息未找到'};
										}
										jQuery('#noticeModal').modal();
										break;
								}
							}
						};
					}(),
					member: function () {
						return {
							add: function (member) {
								if (angular.isObject(member)) {
									// $scope.r_members.members.push(member);
									var members = $scope.$storage.members;
									var memberInMembers = false;
									for (var i=0; i<members.length; i++) {
										if (members[i].member_id == member.member_id) {
											memberInMembers = true;
										}
									}
									if (!memberInMembers) {
										members.push(member);
									}
								};
							},
							get: function (member_id) {
								var members = $scope.$storage.members;
								if (angular.isDefined(member_id)) {
									for (var i=0; i<members.length; i++) {
										if (members[i].member_id == member_id) {
											return members[i];
										}
									}
									return [];
								} else {
									return members;
								}
							},
							remove: function (member_id) {
								for (var i=0; i<$scope.$storage.members.length; i++) {
									if ($scope.$storage.members[i].member_id==member_id) {
										$scope.$storage.members.splice(i, 1);
									}
								}
							},
							removeAll: function () {
								 $scope.$storage.members = [];
							},
							count: function () {
								return $scope.$storage.members.length;
							},
							clear: function () {
								$scope.$storage.members = [];
							}
						};
					}(),
					sms: function () {
						return {
							phoneNumbers: [],
							smsTemplate: '',
							showDialog: function () {
								jQuery('#SMSModal').modal();
							},
							send: function () {
								$http.post('/sms', {phone_nos: this.sms.phoneNumbers, smsTemplate: this.sms.smsTemplate}).success(function(data){
									if (data.success) {
										layer.confirm('是否清空已选择的会员信息?', function(){
											$scope.$storage.members = [];
										});
									}
								});
							}
						};
					}()
				};
			}();
		}
	])

	.controller('HomeCtrl', ['$scope', '$http', function($scope, $http){

	}])

	.controller('UserCtrl', ['$scope', '$http', 'REST', 'Form', 'Pagination', 'Store',
		function($scope, $http, REST, Form, Pagination, Store) {
			$scope.user = {};
			$scope.menu = {action: 'list'};
			$scope.query = {page: 1,limit: 10};
			$scope.belongs = Store.unitList.get({page: 1,limit: 9999});

			// 设置当前的状态
			$scope.setAction = function(action) {
				$scope.menu.action = action;
			};

			// 获取表单的必须数据
			$scope.unitStore = Store.unitList.get({page:1, limit: 9999});

			$scope.showList = function(page) {
				$scope.query.page = page;
				$http.get('/user', {params:$scope.query}).success(function(data) {
					$scope.setAction('list');
					$scope.userStore = data;
					$scope.pager = Pagination(data.total, data.page, data.limit);
				});
			};

			// 显示更新操作窗口
			$scope.update = function(index) {
				$scope.menu.action = 'update';
				$scope.user = $scope.userStore.data[index];
			};

			// 执行更新操作
			$scope.submit = function() {
				var msg = $scope.menu.action == 'add' ? '确定添加此用户么?' : '确定修改此用户么?';
				var url = '';
				var method = '';
				if ($scope.menu.action == 'add') {
					url = '/user';
					method = 'post';
				} else if ($scope.menu.action == 'update') {
					url = '/user/' + $scope.user.user_no;
					method = 'put';
				}
				Form.submit(url, $scope.user, msg, method);
			};

			$scope.setUserStatus = function(user_no) {
				$http.delete('/user/' + user_no).success(function(data){
					$scope.showList($scope.query.page);
				});
			};

			$scope.showList(1);
		}
	])

	.controller('UnitInterCtrl', ['$scope', '$http', 'Pagination',
		function($scope, $http, Pagination) {
			$scope.menu = {
				action: 'list'
			};
			$scope.query = {
				page: 1,
				limit: 10
			};

			$scope.setAction = function(action) {
				$scope.menu.action = action;
			};

			$scope.showList = function(page) {
				$scope.query.page = page;
				$http.get('/unit/inter', {params:$scope.query}).success(function(data) {
					$scope.interStore = data;
					$scope.menu.action = 'list';
					$scope.pager = Pagination(data.total, data.page, data.limit);
				});
			};

			$scope.submit = function(interInfo) {
				$http.post('/unit/inter', interInfo).success(function(data) {
					layer.alert(data.msg);
				});
			};

			// 获取集团信息用以填充表单下拉菜单
			$http.get('/unit', {params: {page: 1,limit: 9999}}).success(function(data) {
				$scope.units = data.data;
			});

			$scope.delete = function(inter_id){
				$http.delete('/unit/inter/'+inter_id).success(function(data){
					$scope.showList($scope.query.page);
				});
			};

			$scope.showList(1);
		}
	])

	.controller('UnitCtrl', ['$scope', '$http', 'Form', 'Pagination',
		function($scope, $http, Form, Pagination) {
			$scope.unit = {};
			$scope.menu = { action: 'list' };
			$scope.query = { page: 1, limit: 10 };

			$scope.setAction = function(action) {
				$scope.menu.action = action;
			};

			$scope.showList = function(page) {
				$scope.query.page = page;
				$http.get('/unit', {params:$scope.query}).success(function(data) {
					$scope.unitStore = data;
					$scope.setAction('list');
					$scope.pager = Pagination(data.total, data.page, data.limit);
				});
			};

			// 显示更新操作窗口
			$scope.update = function(index) {
				$scope.menu.action = 'update';
				$scope.unit = $scope.unitStore.data[index];
			};

			// 执行更新操作
			$scope.submit = function() {
				var msg = $scope.menu.action == 'add' ? '确定添加此集团么?' : '确定修改此集团么?';
				var url = '';
				var method = '';
				if ($scope.menu.action == 'add') {
					url = '/unit';
					method = 'post';
				} else if ($scope.menu.action == 'update') {
					url = '/unit/' + $scope.unit.unit_no;
					method = 'put';
				}
				Form.submit(url, $scope.unit, msg, method);
			};

			$scope.setUnitStatus = function(unit_no) {
				$http.delete('/unit/' + unit_no).success(function(data){
					$scope.showList($scope.query.page);
				});
			};

			$scope.showList(1);
		}
	])

	.controller('ShopCtrl', ['$scope', '$http', 'Store', 'Form', 'Pagination', 'REST',
		function($scope, $http, Store, Form, Pagination, REST) {
			$scope.shop = {};
			$scope.menu = { action: 'list' };
			$scope.query = { page: 1, limit: 10 };
			$scope.pager = {};
			$scope.setAction = function(action) {
				if (action.toLowerCase() == 'add') {
					//$scope.unitStore = Store.unit.get({ page: 1, limit: 9999});
					$scope.unitStore = Store.unitList.get({page: 1, limit: 9999});
				}
				$scope.menu.action = action;
			};

			// 显示更新操作窗口
			$scope.update = function(index) {
				$scope.menu.action = 'update';
				$scope.shop = $scope.shopStore.data[index];
			};

			// 执行更新操作
			$scope.submit = function() {
				var msg = $scope.menu.action == 'add' ? '确定添加此商户么?' : '确定修改此商户么?';
				var url = '';
				var method = '';
				if ($scope.menu.action == 'add') {
					url = '/shop';
					$http.post(url, $scope.shop);
				} else if ($scope.menu.action == 'update') {
					url = '/shop/'+$scope.shop.shop_no;
					$http.put(url, $scope.shop);
				}
			};

			$scope.showList = function(page) {
				$scope.query.page = page;
				$http.get('/shop', {params:$scope.query}).success(function(data, status, headers, config) {
					$scope.shopStore = data;
					$scope.pager = Pagination(data.total, data.page, data.limit);
					$scope.menu.action = 'list';
				});
			};

			$scope.setShopStatus = function(shop_no) {
				$http.delete('/shop/' + shop_no).success(function(data){
					$scope.showList($scope.query.page);
				});
			};
			$scope.showList(1);
		}
	])

	.controller('TerminalCtrl', ['$scope', '$http', 'Form', 'Store', 'Pagination',
		function($scope, $http, Form, Store, Pagination) {
			$scope.terminal = {};
			$scope.menu = {
				action: 'list'
			};
			$scope.query = {
				page: 1,
				limit: 10
			};
			$scope.units = Store.unitList.get({
				page: 1,
				limit: 9999
			});
			$scope.shops = Store.shopList.get({
				page: 1,
				limit: 9999
			});
			$scope.pager = {};

			$http.get('/terminal/trans/code').success(function(data) {
				$scope.trans = data;
			});

			$scope.setAction = function(action) {
				$scope.menu.action = action;
			};

			$scope.showList = function(page) {
				$scope.query.page = page;
				$http.get('/terminal', {
					params: $scope.query
				}).success(function(data) {
					$scope.terminalListStore = data;
					$scope.pager = Pagination(data.total, data.page, data.limit);
					$scope.setAction('list');
				});
			};

			// 显示更新操作窗口
			$scope.update = function(index) {
				$scope.menu.action = 'update';
				$scope.terminal = $scope.terminalListStore.data[index];
			};

			// 执行更新操作
			$scope.submit = function() {
				var msg = $scope.menu.action == 'add' ? '确定添加此终端么?' : '确定修改此终端么?';
				var url = '';
				var method = '';
				if ($scope.menu.action == 'add') {
					url = '/terminal';
					method = 'post';
				} else if ($scope.menu.action == 'update') {
					url = '/terminal/' + $scope.terminal.terminal_no;
					method = 'put';
				}
				$http({
					method: method,
					url: url,
					data: $scope.terminal
				}).success(function(data) {
					layer.alert(data.msg);
				});
			};

			// 根据集团显示商户
			$scope.change = function() {
				$scope.shops = Store.shopList.get({
					page: 1,
					limit: 9999,
					unit_no: $scope.terminal.unit_no
				});
			};

			$scope.setTerminalStatus = function(terminal_no) {
				$http.delete('/terminal/' + terminal_no).success(function(data){
					$scope.showList($scope.query.page);
				});
			};

			$scope.showList(1);
		}
	])

	.controller('CardInfoCtrl', ['$scope', '$http', 'Form', 'Store', 'Pagination',
		function($scope, $http, Form, Store, Pagination) {
			$scope.query = {
				card_no: '',
				page: 1,
				limit: 10
			};
			$scope.menu = {
				action: 'search'
			};

			// 查询卡信息
			$scope.showList = function(query) {
				$http.get('/card', query).success(function(data) {
					$scope.cardStore = data;
					$scope.pager = Pagination(data.total, data.page, data.limit);
					$scope.menu.action = 'list';
				});
			};

			// 设置页面显示状态
			$scope.setAction = function(action) {
				$scope.menu.action = action;
			};

			// 设置卡状态(冻结|解冻),设置成功后更新页面列表中的卡信息
			$scope.setCardStatus = function(index, action) {
				var card_info = $scope.cardStore.data[index];
				$http.put('/card/'+card_info.card_no, {
					action: action
				}).success(function(data) {
					if (data.success) {
						$scope.cardStore.data[index].status = data.data[0].status;
					}
					bootbox.alert(data.msg); // 显示操作结果
				});
			};

			// 用户添加原来的 *自发卡*, 特点是磁道数据就是卡号
			$scope.addNewCard = function(newCard) {
				$http.post('/card', newCard).success(function(data){
					$scope.newCard = {};
				});
			};
		}
	])

	.controller('CardGroupCtrl', ['$scope', '$http', 'Pagination', 'REST',
		function($scope, $http, Pagination, REST) {
			$scope.menu = { action: 'list' };
			$scope.query = { page: 1, limit: 10 };
			$scope.addCardGroupForm = {};

			$scope.setAction = function(action) {
				if (action.toLowerCase()=='set') {
					$scope.groupStore = REST.CardGroup.query({page: 1, limit: 999});
				}
				$scope.menu.action = action;
			};

			$scope.set = function(cardGroup) {
				$http.post('/card/group', cardGroup).success(function(data) {
					layer.alert(data.msg);
					if (!data.success) {
						return;
					}
				});
			};

			$scope.showList = function(page) {
				$http.get('/card/group', {
					params: $scope.query
				}).success(function(data) {
					if (data.success) {
						$scope.groupStore = data;
						$scope.menu.action = 'list';
						$scope.pager = Pagination(data.total, data.page, data.limit);
					} else {
						layer.alert(data.msg);
					}
				});
			};

			$scope.add = function(addCardGroupForm) {
				$http.post('/card/group', addCardGroupForm).success(function(data) {
					layer.alert(data.msg);
					if (!data.success) return;
					$scope.refresh();
				});
			};

			$scope.showList(1);
		}
	])


	// .controller('CardDiscountCtrl', ['$scope', '$http',
	// 	function($scope, $http) {
	// 		$scope.menu = {
	// 			action: 'list'
	// 		};

	// 		$scope.showAddForm = function() {
	// 			// 获取卡组信息
	// 			$http.get('/card/group/list', {
	// 				params: {
	// 					page: 1,
	// 					limit: 9999
	// 				}
	// 			}).success(function(data) {
	// 				$scope.cardGroupStore = data;
	// 			});

	// 			// 获取商户信息
	// 			$http.get('/shop/list', {
	// 				params: {
	// 					page: 1,
	// 					limit: 9999
	// 				}
	// 			}).success(function(data) {
	// 				$scope.shopStore = data;
	// 			});

	// 			$scope.menu.action = 'add';
	// 		}

	// 		$scope.addDiscount = function(discount) {

	// 		}
	// 	}
	// ])

	.controller('CardTransCtrl', ['$scope', 'Form', 'Store', '$http',
		function($scope, Form, Store, $http) {
			$scope.menu = {
				action: 'search'
			};
			$scope.setAction = function(action) {
				$scope.menu.action = action;
			};
			$scope.trans = Store.getTransDim();

			$scope.query = {
				page: 1,
				limit: 10
			};

			$scope.showList = function(page) {
				$scope.query.page = page;
				$http.get('/card/' + $scope.query.card_no + '/trans', {
					params: $scope.query
				}).success(function(data) {
					if (!data.success) {
						layer.alert(data.msg);
						return;
					}
					$scope.transListStore = data;
					$scope.menu.action = 'list';
				});
			};
		}
	])

	.controller('UnitTransMxReportCtrl', ['$scope', '$http', 'Form', 'Store',
		function($scope, $http, Form, Store) {
			$scope.menu = {
				action: 'search'
			};
			$scope.setAction = function(action) {
				$scope.menu.action = action;
			};

			// Search From
			$scope.query = {
				page: 1,
				limit: 10
			};
			$scope.units = Store.unitList.get({
				page: 1,
				limit: 9999
			});
			$scope.transDim = Store.getTransDim();

			$scope.showList = function(page) {
				$scope.query.page = page;
				$http.get('/report/unit/mx', {
					params: $scope.query
				}).success(function(data) {
					$scope.transResultStore = data;
					$scope.menu.action = 'list';
				});
			};
		}
	])

	.controller('ShopTransMxReportCtrl', ['$scope', '$http', 'Store',
		function($scope, $http, Store) {
			$scope.menu = {
				action: 'search'
			};
			$scope.setAction = function(action) {
				$scope.menu.action = action;
			};

			$scope.query = {
				page: 1,
				limit: 10
			};

			$scope.showList = function(page) {
				$scope.query.page = page;
				$http.get('/report/shop/mx', {
					params: $scope.query
				}).success(function(data) {
					$scope.transListStore = data;
					$scope.menu.action = 'list';
				});
			};

			$scope.getShopByUnit = function(unit_no) {
				$http.get('/shop', {
					params: {
						unit_no: unit_no,
						page: 1,
						limit: 9999
					}
				}).success(function(data) {
					$scope.shops = data;
				});
			};

			$scope.units = Store.unitList.get({
				page: 1,
				limit: 9999
			});
			$scope.transDim = Store.getTransDim();
			$scope.shops = $scope.getShopByUnit();
		}
	])

	.controller('TerminalTransMxReportCtrl', ['$scope', '$http', 'Store',
		function($scope, $http, Store) {
			$scope.menu = {
				action: 'search'
			};
			$scope.query = {
				page: 1,
				limit: 10
			};
			$scope.transDim = Store.getTransDim();

			$scope.showList = function(page) {
				$scope.query.page = page;
				$http.get('/report/terminal/mx', {
					params: $scope.query
				}).success(function(data) {
					$scope.transListStore = data;
					$scope.menu.action = 'list';
				});
			};

		}
	])

	.controller('RoleCtrl', ['$scope', '$http', 'Pagination',
		function($scope, $http, Pagination) {
			$scope.menu = {
				action: 'add'
			};
			$scope.role = {};
			$scope.grantInfo = {};
			$scope.pager = {};

			$scope.setAction = function(action) {
				$scope.menu.action = action;
			};

			// 设置form中要用到的operations
			$http.get('/role/operations').success(function(data) {
				$scope.operations = data;
			});

			// 添加或更新role
			$scope.submitRoleForm = function(role) {
				var method = $scope.menu.action == 'add' ? 'POST' : 'PUT';
				var url = $scope.menu.action == 'add' ? '/role' : '/role/' + $scope.role.role_no;
				$http({
					method: method,
					url: url,
					data: role
				}).success(function(data) {
					layer.alert(data.msg);
				});
			};

			// 列出role
			$scope.showList = function() {
				$scope.setAction('list');
				$http.get('/role').success(function(data) {
					$scope.roleStore = data;
					$scope.pager = Pagination(data.total, data.page, data.limit);
				});
			};

			// 授权
			$scope.grantRole = function() {
				// 加载用户信息
				$http.get('/user', {
					params: {
						limit: 9999,
						page: 1
					}
				}).success(function(data) {
					$scope.users = data;
				});

				// 加载权限信息
				$http.get('/role', {
					params: {
						page: 1,
						limit: 9999
					}
				}).success(function(data) {
					$scope.roles = data;
				});

				$scope.setAction('grant');
			};

			// 授权列表
			$scope.grantList = function() {
				$scope.setAction('grantList');
				// 加载授权信息
				$http.get('/role/grant').success(function(data) {
					$scope.grantListStore = data;
					$scope.pager = Pagination(data.total, data.page, data.limit);
				});
			};

			$scope.submitGrantForm = function(grantInfo) {
				$http.post('/role/grant', grantInfo).success(function(data) {
					layer.alert(data.msg);
				});
			};

			$scope.getOperations = function (typeCode) {
				for (var i = 0; i < $scope.operations.length; i++) {
					if ($scope.operations.type_code == typeCode) {
						return $scope.operations[i].operations;
					}
				}
			};

		}
	])

	.controller('GoodsCtrl', ['$scope', '$http', 'Store',
		function($scope, $http, Store) {
			$scope.menu = {action: 'add'};
			$scope.goods = {};
			$scope.query = {page: 1, limit: 10};
            $scope.treeSource = [];
            $scope.branch = null;

			$scope.setAction = function(action) {
				$scope.menu.action = action;
			};

            // 初始化树
            var tree;
            $scope.tree = tree = {};
            $http.get('/goods/class').success(function(resp) {
                if (resp.success){
                    var data = resp.data;
                    var dataSource = [];
                    for (var i=0; i<data.length; i++) {
                        dataSource.push({label: data[i].class_name, data:{id: data[i].id}, children: []});
                    }
                    $scope.treeSource = dataSource;
                }
            });

            $http.get('/supplier').success(function(resp) {
                $scope.supplierStore = resp;
            });

            // 显示添加商品基本信息的表单
            $scope.showAddGoodsForm = function() {
                $('#addGoodsInfoModal').modal();
            }

            // 显示添加商品分类modal
            $scope.showAddClassModal = function() {
                $scope.menu.action = 'add';
                $('#addClassModal').modal();
            }

            /*
             * 显示子节点
             */
            $scope.showChildNode = function(branch) {
                $scope.branch = branch;
                var id = "";
                var b = null;
                if(branch != null) {
                    id = branch.data.id;
                    $scope.goods.class_id = id;
                    b = $scope.tree.get_selected_branch();
                }
                // 获取子节点并显示
                $http.get('/goods/class?id=' + id).success(function(resp){
                    var data = resp.data;
                    $scope.tree.del_all_branch(b);
                    for (var i=0; i<data.length; i++){
                        $scope.tree.add_branch(b, {label: data[i].class_name, data: {id: data[i].id}, children: []});
                    }
                });
                // 获取当前点击节点的商户并显示
                $scope.searchGoodsURL = '/goods/info/base' + '?class_id=' + id;
            }

            // 添加分类
            $scope.addGoodsClass = function(isRoot) {
                var msg = '准备添加根分类，请输入分类名称：';
                if(isRoot!=true) {
                    msg = '准备为' + $scope.branch.label + '添加子分类，请输入分类名称：';
                }
                bootbox.prompt(msg, function(className) {
                    if(className == null) {
                    } else {
                        var pid = isRoot == true ? '' : $scope.branch.data.id;
                        className = $.trim(className);
                        if(className.length > 0) {
                            console.log('add class -> ' + className);
                            $http.post('/goods/class', {pid: pid, class_name: className})
                                    .success(function(resp) {
                                        if(resp.success) {
                                            $scope.showChildNode($scope.branch);
                                        }
                                    });
                        }
                    }
                });
            }

			// 添加商品
			$scope.addGoods = function(goods) {
				if ($scope.menu.action == 'add') {
                    var result = Store.goodsBaseInfoList.add(goods, function(){
                        if (result.success) {
                            $scope.collection = Store.goodsBaseInfoList.get({class_id: goods.class_id});
                            $('#addGoodsInfoModal').modal('hide');
                        }
                    });
				} else {
					$http.put('/goods/info/base/' + goods.id, goods).success(function(data) {
						layer.alert(data.msg);
					});
				}
			};

			// 显示商品列表
			$scope.showList = function(page) {
				$scope.query.page = page;
				$http.get('/goods/info/base', {
					params: $scope.query
				}).success(function(data) {
					$scope.menu.action = 'list';
					$scope.goodsStore = data;
					$scope.pager = Pagination(data.total, data.page, data.limit);
				});
			};

			// 修改商品信息
			$scope.update = function(index) {
				$scope.goods = $scope.goodsStore.data[index];
				$scope.goods.price = $scope.goods.price / 100.00;
				$scope.menu.action = 'update';
			};

			// ********* 商品入库 *********
			// 显示表单
//			$scope.showReverseForm = function() {
//				$scope.menu.action = 'storage';
//				$http.get('/goods/baseinfo', {params:{
//					limit: 9999
//				}}).success(function(data) {
//					$scope.goodsStore = data;
//				});
//			};
//			// 提交入库信息
//			$scope.submitReverse = function(storage) {
//				$http.post('/warehouse/recepit', storage);
//			};
		}
	])

	.controller('SaleCtrl', ['$scope', '$http', 'Pagination',
		function($scope, $http, Pagination) {
			$scope.menu = {action: 'sale'};
			$scope.query = {page: 1, limit: 10};
			$scope.setAction = function(action) {
				$scope.menu.action = action;
			};

			// **********
			// 初始化各项
			//
			function init() {
				$scope.order = []; // 订单
				$scope.orderItem = {}; // 订单中的每项商品
				$scope.payment = { // 支付方式
					order_id: '',  // 要支付的订单ID
					amount: 0,  // 这里的amount是分
					mode: 'card',  // card cash mixed 四种方式
					card: {  // 使用卡支付的部分
						card_no: '',
						track_2: '',
						password: '',
						amount: 0  //这里的amount是元, 要在后台换算！！！
					},
					cash: {  // 使用现金支付的部分
						amount: 0  //这里的amount是元, 要在后台换算！！！
					}
				};
			}

			init();

            $scope.newSale = function() {
                $scope.menu.action = 'sale';
                init();
            }

			// 提交订单
			$scope.submitOrder = function(order) {
				$http.post('/sale/order', {
					'order': order
				}).success(function(data) {
                    if(!data.success) {
                        bootbox.alert(data.msg);
                        return;
                    }
					$scope.payment.order_id = data.data.order_id;
					$scope.payment.amount = data.data.amount;
					$.layer({
						type: 1,
						title: ['', false],
						fix: false,
						offset: ['50px', ''],
						area: ['600px', '300px'],
						border: [8, 0.3, '#000', false],
						page: {
							dom: '#payForm'
						}
					});
				});
			};

            $scope.getOrderTotalPay = function() {
                var total = 0;
                for(var i=0; i<$scope.order.length; i++) {
                    total += $scope.order[i].discounted_money_amount;
                }
                return total;
            }

			// 支付,此处是已提交订单,根据返回的订单号进行支付
			$scope.pay = function(payment) {
				if (payment.mode == 'card') {
					payment.card.amount = payment.amount / 100.00;
				}
				$http.put('/sale/order/' + payment.order_id + '/pay', payment).success(function(data) {
					if (data.success) {  // 支付成功
						layer.closeAll();
						init();
						printer.print(data.ticket.content, data.ticket.length);
					}
				});
			};

			$scope.splitCard = function(raw_card_no) {
				// 将刷卡信息分成两部分：卡号和二磁道信息
				var splited_card_no = raw_card_no.split('=');
				$scope.payment.card.card_no = splited_card_no[0];
				$scope.payment.card.track_2 = raw_card_no;
			};


			function addItem2Order(orderItem) {
				// 将商品添加到订单中.如果商品已在订单中出现,则直接修改订单中的商品数量,
				// 避免出现同一种商品出现在订单列表中多行的现象
				// 2014.06.06: 不再合并同类商品
//                $scope.payment.amount += orderItem.discounted_money_amount * 100;
//                var goods_id = orderItem.goods_id;
//                var itemInOrder = false;
//                for (var i = 0; i < $scope.order.length; i++) {
//                    if ($scope.order[i].goods_id == goods_id) {
//                        $scope.order[i].goods_amount += orderItem.goods_amount;
//                        itemInOrder = true;
//                        break;
//                    }
//                }
//                if (!itemInOrder) {
					$scope.order.push(orderItem);
//                }
			}

			// 添加商品到订单时,根据商品的关键字查找商品.
			// 如果找到一个,则直接添加到订单中;如果找到多个,则需要售货员从列表中选择
			$scope.searchSaleGoods = function(saleKeyword) {
                var url = '/goods?action=sale&keyword=' + $.trim(saleKeyword);
				$http.get(url).success(function(data) {
					var orderItem = {
						goods_id: '',
						goods_name: '',
						price: 0,
						goods_amount: 0,
						money_amount: 0,
						discount: 100
					};

					if (data.total == 0) {
						layer.alert('未找到合适的商品');
						return;
					} else if (data.total == 1) { // 只有一件商品,直接添加了订单列表中
						var g = data.data[0];
						orderItem.goods_id = g.id;
						orderItem.goods_name = g.goods_name;
						orderItem.price = g.sale_price / 100;
						orderItem.goods_amount = 1;
						orderItem.discount = 100;
						orderItem.money_amount = orderItem.price * orderItem.goods_amount;
						orderItem.discounted_money_amount = orderItem.money_amount * orderItem.discount / 100;
						$scope.orderItem = orderItem;
						addItem2Order(orderItem);
					} else if(data.total > 1) {
//						$scope.multiGoodsFoundTableStore = data;
                        $scope.multiGoodsFoundUrl = url;
						$('#multiGoodsFoundModal').modal();
					}
				});
			};

			// 添加售货员选择的商品
			$scope.addMultiTableGoods = function(index) {
				var orderItem = {
					goods_id: '',
					goods_name: '',
					price: 0,  // 定价
					sale_price: 0,  // 实际售价
					goods_amount: 0,
					money_amount: 0,  // 实际售价总额
					discounted_money_amount: 0  // 折后总额
				};
				var g = $scope.multiGoodsFoundTableStore.data[index];
				orderItem.goods_id = g.id;
				orderItem.goods_name = g.goods_name;
				orderItem.price = g.sale_price / 100.00;
				orderItem.goods_amount = 1;
				orderItem.discount = 100;
				orderItem.money_amount = orderItem.price * orderItem.goods_amount;
				orderItem.discounted_money_amount = orderItem.money_amount * orderItem.discount / 100;
				$scope.orderItem = orderItem;
				addItem2Order(orderItem);
			};

			// 计算折后金额
			$scope.calculateAmount = function (goods_id) {
				for(var i=0; i<$scope.order.length; i++) {
					var order = $scope.order[i];
					if(order.goods_id == goods_id) {
						order.money_amount = order.price * order.goods_amount;
						order.discounted_money_amount = order.money_amount * order.discount / 100.00;
					}
				}
			};

			// 显示订单列表
			$scope.showOrderList = function(page) {
				$scope.query.page = page;
				$http.get('/sale/order', {
					params: $scope.query
				}).success(function(data) {
					$scope.orderStore = data;
					$scope.menu.action = 'orderList';
					$scope.orderListPager = Pagination(data.total, data.page, data.limit);
				});
			};

			// 显示订单明细
			$scope.showOrderDetail = function(order_id){
				$http.get('/sale/order/detail/' + order_id)
					 .success(function(data){
						$scope.orderDetailStore = data;
						$scope.menu.action = 'orderDetail';
					 });
			};
		}
	])

	.controller('MemberCtrl', ['$scope', '$http', 'Pagination',
		function($scope, $http, Pagination) {
			$scope.menu = { action: 'list' };
			$scope.query = { page: 1, limit: 10 };
			$scope.smsQuery = { page: 1, limit: 10 };
			$scope.member = {
				card:{}
			};

			$scope.getCardInfo = function(card_no) {
				/* 根据卡BIN判断是系统卡还是客户的自发卡
					 如果是客户自发卡，则显示附加信息*/
				card_no = card_no.trim();
				if (card_no.length==19 && card_no.substr(0,3)==g.card_bin) {  // 系统卡
					$scope.member.card.type = 'sys';
				} else {
					$scope.member.card.type = 'custom';
				}

			};

			$scope.setAction = function(action) {
				action = action.toLowerCase();
				switch (action) {
					case 'add':
						// 加载商户信息
						$http.get('/shop?limit=9999').success(function(data) {
							$scope.shopStore = data;
						});
						break;
					case 'list':
						$scope.query = {page: 1, limit: 10};
				}
				$scope.menu.action = action;
			};

			$scope.showList = function(page) {
				$scope.query.page = page;
				$http.get('/member', {
					params: $.extend(false, $scope.query, $scope.member)
				}).success(function(data) {
					for(var i=0; i<data.data.length; i++) {
						if ($.inArray(data.data[i].phone, $scope.$storage.members) != -1) {
							data.data[i].checked = true;
						} else {
							data.data[i].checked = false;
						}
					}
					$scope.memberStore = data;
					$scope.pager = Pagination(data.total, data.page, data.limit);
					$scope.menu.action = 'list';
				});
			};

			// 为会员添加卡
			$scope.addCard = function() {
				if (angular.isElement($scope.cards)) {
					$http.post('/member/card/add', {
						data: $scope.cards
					}).success(function(data) {

					});
				} else {
					layer.alert('请先添加卡');
				}
			};

			$scope.addOrUpdate = function(member) {
				var method = $scope.menu.action == 'add' ? 'POST' : 'PUT';
				var url = $scope.menu.action == 'add' ? '/member' : '/member/' + $scope.member.member_id;
				if ($scope.menu.action=='add' && member.card.type=='custom') {
					if(member.card.password.trim() != member.card.repassword.trim()){
						layer.alert('两次输入的密码不一致');
						return;
					}
				}
				$http({
					url: url,
					method: method,
					data: member
				}).success(function(data) {
					layer.alert(data.msg);
				});
			};

			$scope.addToMemberList = function(index) { // 添加到会员列表
				var member = $scope.memberStore.data[index];
				$scope.root.member.add(member);
			};

			$scope.selectMember = function (type) {
				// type = all(全选)/reverse(反选)/cancel(取消选择)
				var data = $scope.memberStore.data;
				for (var i=0; i<data.length; i++) {
					switch (type) {
						case 'all':
							data[i].checked = true;
							break;
						case 'reverse':
							data[i].checked = !data[i].checked;
							break;
						case 'cancel':
							data[i].checked = false;
							break;
					}
				}
			};

			$scope.addSelectedMembersToList = function () {
				var data = $scope.memberStore.data;
				for (var i=0; i<data.length; i++) {
					if (data[i].checked) {
						$scope.root.member.add(data[i]);
					}
				}
				$scope.root.notice.set({
					id: '58ddedb3-4ad6-4f44-84bc-f1209a9bc47b',
					title: '您有'+$scope.root.member.count()+'条会员信息需要处理',
					content: '您在会员列表中选择了' + $scope.root.member.count()
							 + '条会员信息，您可以在[会员管理][已选会员]菜单中选择相应的操作',
					event: 'showSelectedMembers'
				});
			};
			$scope.showList(1);
		}
	])

	.controller('SupplierCtrl', ['$scope', '$http', 'Pagination',
		function($scope, $http, Pagination) {
			$scope.menu = {
				action: 'add'
			};
			$scope.query = {
				limit: 10,
				page: 1
			}; // 请求参数

			// 设置当前操作
			$scope.setAction = function(action) {
				$scope.menu.action = action;
			};

			// 添加新供应商或更新
			$scope.submit = function(supplier) {
				var method = $scope.menu.action == 'add' ? 'POST' : 'PUT';
				var url = $scope.menu.action == 'add' ? '/supplier' : '/supplier/' + $scope.supplier.id;
				$http({
					url: url,
					method: method,
					data: supplier
				}).success(function(data) {
					layer.alert(data.msg);
				});
			};

			// 分页显示所有供应商
			$scope.showList = function(page) {
				$scope.query.page = page;
				$http.get('/supplier', {
					params: $scope.query
				}).success(function(data) {
					if (!data.success) {
						layer.alert(data.msg);
						return;
					} else {
						$scope.supplierStore = data;
						$scope.pager = Pagination(data.total, data.page, data.limit);
						$scope.menu.action = 'list';
					}
				});
			};

			// 跳转页面
			$scope.loadPage = function(page) {
				$scope.query.page = page;
				$scope.showList();
			};

			// 更新供应商信息
			$scope.update = function(index) {
				$scope.menu.action = 'update';
				$scope.supplier = $scope.supplierStore.data[index];
			};

		}
	])

	.controller('WarehouseCtrl', ['$scope', '$http', 'Pagination',
		function($scope, $http, Pagination) {
			$scope.menu = {
				action: 'add'
			};
			$scope.query = {
				page: 1,
				limit: 10
			};

			$scope.showList = function() {
				$http.get('/warehouse', {
					params: $scope.query
				}).success(function(data) {
					$scope.warehouseStore = data;
					$scope.pager = Pagination(data.total, data.page, data.limit);
					$scope.menu.action = 'list';
				});
			};

			$scope.submit = function(warehouse) {
				if ($scope.menu.action == 'add') {
					$http.post('/warehouse', warehouse);
				} else if ($scope.menu.action == 'update') {
					$http.put('/warehouse/' + $scope.warehouse.id, warehouse);
				}
			};

			$scope.update = function(index) {
				$scope.warehouse = $scope.warehouseStore.data[index];
				$scope.menu.action = 'update';
			};
		}
	])

	.controller('WebPosCtrl', ['$scope', '$http',
		function($scope, $http) {

			$scope.trans = {
				trans_code: '000010'
			}; // 默认消费交易

			$scope.setTransCode = function(trans_code) {
				$scope.trans.trans_code = trans_code;
			};

			$scope.getTransName = function() {
				var trans_dim = {
					code_000010: '消费',
					code_000030: '充值',
					code_000190: '撤销',
					code_000050: '积分消费',
					code_000070: '积分充值',
					code_000110: '卡启用',
					code_000120: '换卡',
					code_000090: '查询余额',
					code_000140: '卡改密码',
					code_000150: '卡改有效期'
				};
				return trans_dim['code_' + $scope.trans.trans_code];
			};

			$scope.show = function(input) {
				var showControl = {
					code_000010: ['ipt_card_no', 'ipt_amount', 'ipt_password'],
					code_000030: ['ipt_card_no', 'ipt_amount'],
					code_000190: ['ipt_card_no', 'ipt_batch_no', 'ipt_trace_no', 'ipt_password'],
					code_000050: ['ipt_card_no', 'ipt_amount', 'ipt_password'],
					code_000070: ['ipt_card_no', 'ipt_amount', 'ipt_password'],
					code_000110: ['ipt_card_no', 'ipt_password'],
					code_000090: ['ipt_card_no', 'ipt_password'],
					code_000140: ['ipt_card_no', 'ipt_password', 'ipt_new_password', 'ipt_renew_password'],
					code_000150: ['ipt_card_no', 'ipt_password', 'ipt_exp_date']
				};
				var ctrl = showControl['code_' + $scope.trans.trans_code];
				return $.inArray(input, ctrl) >= 0 ? true : false;
			};

			$scope.setTrack2 = function(track2) {
				track2 = track2.trim();
				if (track2.length == 37) {
					$scope.trans.card_no = track2.substr(0, 18);
					$scope.trans.track_2 = track2;
					layer.alert($scope.trans.card_no);
				}
			};

			$scope.doTrans = function(transForm) {
				$http.post('/webtrans', $scope.trans)
					.success(function(data) {
						if (data.success) {
							printer.print(data.data.print_text);
						}
						else
						{
							layer.alert(data.msg);
						}
					});
			};
		}
	])

	.controller('SMSCtrl', ['$scope', '$http', 'Pagination', function ($scope, $http, Pagination) {
		$scope.menu = {action: 'list'};
		$scope.query = {page: 1, limit: 10};
		$scope.setAction = function (action) {$scope.menu.action = action;};

		$scope.showList = function(page) {
			$scope.query.page = page;
			$http.get('/sms/template', {params: $scope.query}).success(function(data){
				$scope.templateStore = data;
				$scope.pager = Pagination(data.total, data.page, data.limit);
				$scope.menu.action = 'list';
			});
		};

		$scope.submit = function(template) {
			if ($scope.menu.action == 'add') {
				$http.post('/sms/template', $scope.template);
			} else if ($scope.menu.action == 'update') {
				$http.put('/sms/template/' + $scope.template.id, $scope.template);
			}
		};

		$scope.update = function (index) {
			$scope.template = $scope.templateStore.data[index];
			$scope.menu.action = 'update';
		};

		$scope.addToTemplateContent = function(vars) {
			if (!angular.isDefined($scope.template)) {
				$scope.template = {};
			}
			if (vars != '') {
				$scope.template.content += vars;
			}
		};

		$scope.showList(1);

	}])

	.controller('AccountSettingsCtrl', ['$scope', '$http', function ($scope, $http) {
		$http.get('/settings/account').success(function(response){
			$scope.settings = response.data;
		});
	}])

	.controller('SysSettingsCtrl', ['$scope', '$http', function ($scope, $http) {
		$scope.setTicket = function(ticket){

		};
	}])

	.controller('WeiXinSettingCtrl', ['$scope', '$http', function($scope, $http) {
		// 获取微信token并显示
		$http.get('/settings/weixin/token').success(function(resp){
			$scope.token = resp.token;
		});
	}])

	.controller('SizeGroupCtrl', ['$scope', '$http', 'Pagination', function ($scope, $http, Pagination) {
		$scope.menu = {action: 'add'};
		$scope.query = {page: 1, limit: 10};

		// 添加尺寸信息
		$scope.submitSizeGroup = function(sizeGroup) {
			$http.post('/size/group', sizeGroup);
		};

		// 显示尺寸组列表
		$scope.showSizeGroupList = function(){
			$http.get('/size/group', {params: $scope.query}).success(function(resp){
				if (resp.success) {
					$scope.menu.action = 'list';
					$scope.sizeGroupStore = resp;
					$scope.pager = Pagination(resp.total, resp.page, resp.limit);
				}
			});
		};
	}])

	.controller('PurchaseOrderCtrl', ['$scope', '$http', 'Store', function($scope, $http, Store) {
		function init() {
			$scope.id = '';  // 当前操作的商品id
			$scope.branch = null;  // 当前选中的商品分类
			$scope.menu = {action: 'addPurchaseOrder'};
			$scope.goods_class = {id: '', class_name: '', size_group_id: ''};  // 添加分类时要上送的数据
			$scope.purchaseOrder = {data: []};  // 采购明细
//			$scope.selectedGoods = {};  // 从对话框中选择的采购商品
			$scope.goodsSize = ['均码'];  // 用户自行添加的商品号码
            $scope.purchaseOrderListUrl = '/goods/purchase/order';  // 采购订单列表的URL
            $scope.goodsListUrl = '/goods';
		}

		init();

		var goodsClassTree;

		$scope.setAction = function(action) {
			$scope.menu.action = action;
		};

		// 填充商品分类树
		$scope.goodsClassTreeSource = [];  // 当前商品分类信息树数据源
		$scope.goodsClassStore = Store.goodsClassList.get(null, function(resp) {
			var data = resp.data;
			for (var i=0; i<data.length; i++) {
				$scope.goodsClassTreeSource.push({label: data[i].class_name, data:{id: data[i].id}, children: []});
			}
		});

		// 新的进货单
		$scope.newPurchaseOrder = function(){
			$scope.menu.action = 'addPurchaseOrder';
			init();
			$('#chooseGoodsModal').modal();
		};

		// 显示子节点及表格中的商品
		$scope.goodsClassTree = goodsClassTree = {};
		$scope.showChildNode = function(branch) {
			var id = branch.data.id;
			$scope.branch = branch;
			// 获取子节点并显示
			$http.get('/goods/class?id=' + id).success(function(resp){
				var data = resp.data;
				var b = goodsClassTree.get_selected_branch();
				goodsClassTree.del_all_branch(b);
				for (var i=0; i<data.length; i++){
					goodsClassTree.add_branch(b, {label: data[i].class_name, data: {id: data[i].id}, children: []});
				}
			});
			// 获取当前点击节点的商户并显示
			$scope.searchGoodsURL = '/goods/info/base' + '?class_id=' + id;

		};

		// 选择进货商品
		$scope.chooseThis = function(goods_id) {
			$http.get('/goods/info/base?id=' + goods_id).success(function(resp) {
				if(resp.success) {
//					$scope.selectedGoods = resp.data[0];
					$("#chooseGoodsModal").modal('hide');

					var item = {
						id: resp.data[0].id,  // 商品 id
						color: '',  // 商品颜色
                        purchase_price: "0.00",  // 采购价格
                        label_price: "0.00",  // 吊牌价格
                        sale_price: "0.00",  // 零售价格
						goods_name: resp.data[0].goods_name,  // 商品名称
						sizes:{}  // 商品尺寸
                    };

                    // 初始化所选择商品的所有尺寸的进货数量为0
					for(var i=0; i<$scope.goodsSize.length; i++){
						// item[$scope.goodsSize[i]] = 0;
                        item.sizes[$scope.goodsSize[i]] = 0;
					}

					$scope.purchaseOrder.data.push(item);
					console.log(resp);
				}
			});
		}

		$scope.showPurchaseOrderList = function() {
			$http.get('/goods/purchase/order').success(function() {
			    $scope.purchaseOrderListStore = resp;  // 采购单列表
			});
		}

		$scope.showAddClassModal = function() {
			$('#addClassModal').modal();
		}

		$scope.showChooseGoodsModal = function() {
			$('#chooseGoodsModal').modal();
		}

		// 添加分类
		$scope.addClass = function() {
			var msg = '准备添加根分类，请输入分类名称：';
			if($scope.branch != null) {
				msg = '准备为' + $scope.branch.label + '添加子分类，请输入分类名称：';
			}
			bootbox.prompt(msg, function(className) {
				if(className == null) {
				} else {
					var pid = $scope.branch == null ? '' : $scope.branch.data.id;
					className = $.trim(className);
					if(className.length > 0) {
						console.log('add class -> ' + className);
						$http.post('/goods/class', {pid: pid, class_name: className})
								.success(function(resp) {
									if(resp.success) {
										$scope.showChildNode($scope.branch);
									}
								});
					}
				}
			});
		}

		// 添加size
		$scope.addGoodsSize = function(size) {
			bootbox.prompt('请输入要设置的号码', function(size) {
				if(size === null) {
				} else {
					size = $.trim(size);
					if (size.length > 0) {
						console.log('add goods size -> ' + size);
						if($.inArray(size, $scope.goodsSize) == -1) {
                            $scope.goodsSize.push(size);
                            for(var i=0; i<$scope.purchaseOrder.data.length; i++) {
                                $scope.purchaseOrder.data[i].sizes[size] = 0;
                            }
                            $scope.$apply();
                        }
					}
				}
			});
		}

		// 提交进货单
		$scope.submitPurchaseOrder = function() {
			bootbox.confirm('确认提交采购单?', function(result) {
				if (result == false) {
					return;
				}
				$http.post('/goods/purchase/order', {data: $scope.purchaseOrder})
                    .success(function(resp) {
                        if(resp.success) {
                            // bootbox.confirm('是否进行新的采购?', function(result) {
                            //     if(result == true){
                            $scope.newPurchaseOrder();
                            //     }
                            // });
                        }
                    });
			});
		}

		// 显示我的商品信息
		$scope.showGoodsInfo = function() {
			$scope.menu.action = 'showGoodsInfo';
		}

	}])

	.controller('MyProfileCtrl', ['$scope', '$http', 'Store', function ($scope, $http, Store) {
		$http.get('/user/profile').success(function(resp){
			$scope.profile = resp.data[0];
		});
	}])

	.controller('SaleReportCtrl', ['$scope', '$http', 'Store', function ($scope, $http, Store) {
		$scope.saleGoodsStoreUrl = '/sale/report';
		$scope.reportQuery = {
			start_date: new Date(2014,9,1),
			end_date: new Date(2014,9,1)
		};
		$scope.activeButton = 0;  // 指定哪个日期button是激活状态

		$scope.doQuery = function(query) {
			var queryStr = '';
			for(var i in query) {
				queryStr += (i + '=' + query[i] + '&');
			}
			$scope.saleGoodsStoreUrl = $scope.saleGoodsStoreUrl.split('?')[0] + '?' + queryStr;
		}

		$scope.setReportQuery = function(days) {
			$scope.activeButton = days;
			var today = new Date();
			var startDate = new Date();
			startDate.setDate(today.getDate() + days);
			$scope.reportQuery.start_date = startDate.format('yyyyMMdd');
			$scope.reportQuery.end_date = today.format('yyyyMMdd');
			$scope.doQuery($scope.reportQuery);
		}
	}])

	.controller('FeedbackCtrl', ['$scope', '$http', 'Store', function ($scope, $http, Store){
		$scope.suggestionStore = Stroe.feedbackList.get();
	}]);