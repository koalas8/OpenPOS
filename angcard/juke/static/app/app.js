'use strict';

var My = {
	'showLoading': true,
    Cookie: function(){
       return {
           get: function(name) {
               var re = new RegExp(name + '=([^;]*);?', 'gi');
               var r = re.exec(document.cookie) || [];
               return r.length>1 ? r[1] : null
           }
       }
    }()
};

// Declare app level module which depends on filters, and services
angular.module('angcardApp', [
	'ngRoute',
	'angcardApp.filters',
	'angcardApp.services',
	'angcardApp.directives',
	'angcardApp.controllers',
	'ngBootstrap',
	'ngStorage',
	'ngAnimate',
	'angularBootstrapNavTree',
	'jukePaginate',
	'jukeColorPicker',
    'angularSpectrumColorpicker'
])
.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
	var baseUrl = '/static/partials/angcard';
	//$routeProvider.when('/', {templateUrl: baseUrl + '/home.html', controller: 'HomeCtrl'});
	$routeProvider.when('/user', {templateUrl: baseUrl + '/user.html', controller: 'UserCtrl'});
	$routeProvider.when('/role', {templateUrl: baseUrl + '/role.html', controller: 'RoleCtrl'});
	$routeProvider.when('/unit', {templateUrl: baseUrl + '/unit.html', controller: 'UnitCtrl'});
	$routeProvider.when('/shop', {templateUrl: baseUrl + '/shop.html', controller: 'ShopCtrl'});
	$routeProvider.when('/terminal', {templateUrl: baseUrl + '/terminal.html', controller: 'TerminalCtrl'});
	$routeProvider.when('/unit_inter', {templateUrl: baseUrl + '/unit_inter.html', controller: 'UnitInterCtrl'});
	$routeProvider.when('/card/info', {templateUrl: baseUrl + '/card/info.html', controller: 'CardInfoCtrl'});
	$routeProvider.when('/card/group', {templateUrl: baseUrl + '/card/group.html', controller: 'CardGroupCtrl'});
	$routeProvider.when('/card/trans', {templateUrl: baseUrl + '/card/trans.html', controller: 'CardTransCtrl'});
	$routeProvider.when('/card/discount', {templateUrl: baseUrl + '/card/discount.html', controller: 'CardDiscountCtrl'});
	$routeProvider.when('/report/sale', {templateUrl: baseUrl + '/psi/sale_report.html', controller: 'SaleReportCtrl'});
	$routeProvider.when('/report/unit/mx', {templateUrl: baseUrl + '/report/unit_mx.html', controller: 'UnitTransMxReportCtrl'});
	$routeProvider.when('/report/shop/mx', {templateUrl: baseUrl + '/report/shop_mx.html', controller: 'ShopTransMxReportCtrl'});
	$routeProvider.when('/report/terminal/mx', {templateUrl: baseUrl + '/report/terminal_mx.html', controller: 'TerminalTransMxReportCtrl'});
	$routeProvider.when('/member', {templateUrl: baseUrl + '/member.html', controller: 'MemberCtrl'});
	$routeProvider.when('/supplier', {templateUrl: baseUrl + '/psi/supplier.html', controller: 'SupplierCtrl'});
	$routeProvider.when('/warehouse', {templateUrl: baseUrl + '/psi/warehouse.html', controller: 'WarehouseCtrl'});
	$routeProvider.when('/goods', {templateUrl: baseUrl + '/psi/goods.html', controller: 'GoodsCtrl'});
	$routeProvider.when('/sale', {templateUrl: baseUrl +'/psi/sale.html', controller: 'SaleCtrl'});	
	$routeProvider.when('/sizeGroup', {templateUrl: baseUrl + '/psi/size_group.html', controller: 'SizeGroupCtrl'});
    $routeProvider.when('/purchase_order', {templateUrl: baseUrl + '/psi/clothes/purchase_order.html', controller: 'PurchaseOrderCtrl'});
	$routeProvider.when('/webpos', {templateUrl: baseUrl + '/webpos/webpos.html', controller: 'WebPosCtrl'});
	$routeProvider.when('/myprofile', {templateUrl: baseUrl + '/account/myprofile.html', controller: 'MyProfileCtrl'});
	$routeProvider.when('/settings/account', {templateUrl: baseUrl + '/account_setting.html', controller: 'AccountSettingsCtrl'});
	$routeProvider.when('/settings/sys', {templateUrl: baseUrl + '/sys_setting.html', controller: 'SysSettingsCtrl'});
    $routeProvider.when('/settings/weixin', {templateUrl: baseUrl + '/settings/weixin_setting.html', controller: 'WeiXinSettingCtrl'});
	$routeProvider.when('/settings/sms', {templateUrl: baseUrl + '/sms/sms.html', controller: 'SMSCtrl'});
	$routeProvider.when('/feedback', {templateUrl: baseUrl + '/feedback.html', controlloer: 'FeedbackCtrl'});
	
	$locationProvider.hashPrefix('!');
}])
.config(['$httpProvider', function($httpProvider) {
	$httpProvider.interceptors.push(function($q) {
		var loading;
		return {
			'request': function(config) {
				if (My.showLoading){
		 			loading = layer.load('加载中...');
		 		}
				return config || $q.when(config);
			},
			'requestError': function(rejection) {
				layer.close(loading);
				layer.alert('请求数据时出现错误，请重试...');
				// if (canRecover(rejection)) {
				// 	return responseOrNewPromise
				// }
				return $q.reject(rejection);
			},
			'response': function(response) {
				layer.close(loading);
				if(response.data.show_msg) {
					layer.alert(response.data.msg);
				}

				// 如果用户已经退出系统，但是点击了后退按钮，则跳转到登陆页面
				if(angular.isDefined(response.data.redirect_url)) {
					window.location.href=response.data.redirect_url;
				}
				return response || $q.when(response);
			},
			'responseError': function(rejection) {
				layer.close(loading);
				layer.alert('请求数据时出现错误，请重试...');
				// if (canRecover(rejection)) {
				// 	return responseOrNewPromise
				// }
				return $q.reject(rejection);
			}
		};
	});
}])
;