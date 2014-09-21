'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('angcardApp.services', ['ngResource'])
    .factory('Form', ['$http', function ($http) {        
        return {
            submit: function(url, data, msg, method) {
                var confirm_flag = false;
                var confirm_result = true;
                if (msg != null && msg != 'undefined' && msg != '') {
                    confirm_flag = true;
                }

                if (confirm_flag) {
                    if (confirm(msg) == true) {
                        confirm_result = true;
                    }else{
                        return;
                    }
                }

                if (confirm_result) {
                    $http ({
                        method: method,
                        url: url,
                        data: jQuery.toJSON(data)
                    }).success(function(data){
                        bootbox.alert(data.msg);
                        return data.success;                        
                    });
                }
            }    
        };
    }])
    .factory('Store',function ($resource) {
        return {
            user: $resource('/user'),
            operator: $resource('/operator'),
            unit: $resource('/unit',[], {query: {method: 'GET', isArray: false}}),
            unitList: $resource('/unit', {page:1, limit:10}, {
                get: {method: 'GET'},
                add: {method: 'POST'}
            }),
            shop: $resource('/shop'),
            shopList: $resource('/shop', {page: 1, limit: 10}, {
                get: {method: 'GET'},
                add: {method: 'POST'}
            }),
            terminal: $resource('/terminal'),
            terminalList: $resource('/terminal', {page: 1, limit: 10}, {
                get: {method: 'GET'},
                add: {method: 'POST'}
            }),
            cardList: $resource('/card/list'),
            cardTrans: $resource('/card/trans'),
            supplierList: $resource('/supplier', {page: 1, limit: 10}, {
                get: {method: 'GET'},
                add: {method: 'POST'}
            }),
            goodsClassList: $resource('/goods/class', {page: 1, limit: 10}, {
                get: {method: 'GET'},
                add: {method: 'POST'}
            }),

            goodsBaseInfoList: $resource('/goods/info/base', {page: 1, limit: 10}, {
                get: {method: 'GET'},
                add: {method: 'POST'}
            }),
            goodsList: $resource('/goods', {page: 1, limit: 10}, {
                get: {method: 'GET'},
                add: {method: 'POST'}
            }),
            saleOrder: $resource('/sale/order/:order_id', {page: 1, limit: 10}, {
                get: {method: 'GET'},
                update: {method: 'PUT'}
            }),
            saleOrderList: $resource('/sale/order', {page: 1, limit: 10}, {
                get: {method: 'GET'},
                add: {method: 'POST'}
            }),
            saleReport: $resource('/sale/report', {}, {
                get: {method: 'GET'}
            }),
            feedbackList: $resource('/feedback', {page: 1, limit: 10}, {
                get: {method: 'GET'}
            }),


            getTransDim: function(){
                return [{trans_code: '000110', trans_name: '卡启用'},
                        {trans_code: '000010', trans_name: '消费'},
                        {trans_code: '000020', trans_name: '消费撤销'},
                        {trans_code: '000030', trans_name: '充值'},
                        {trans_code: '000040', trans_name: '充值撤销'},
                        {trans_code: '000050', trans_name: '积分消费'},
                        {trans_code: '000060', trans_name: '积分消费撤销'},
                        {trans_code: '000070', trans_name: '积分充值'},
                        {trans_code: '000080', trans_name: '积分充值撤销'}];
            }
        }
    })
    .factory('Pagination', function(){
        return function(total, page, limit){

            var jumps = 10;  // 每页显示10个跳转
            var totalPage = total % limit == 0? parseInt(total/limit): parseInt(total/limit) + 1;  // 共多少页
            var startPage;
            var endPage;
            if (jumps >= totalPage) {
                startPage = 1;
                endPage = totalPage;
            } else {
                startPage = page - parseInt(jumps/2);
                startPage = startPage < 1 ? 1 : startPage;
                endPage = startPage + jumps - 1;
                endPage = endPage > totalPage ? totalPage : endPage;
            }
           
            var pager = {};        
            pager.pages = [];
            if (startPage!=1){
                pager.pages.push({page: 1, label: '首页'});
            }
            for(var i=startPage; i<=endPage; i++){
                pager.pages.push({page: i, 'label': i});
            }
            if (endPage!=totalPage){               
                pager.pages.push({page: totalPage, label: '末页'});
            }
            return pager;
        };
    })
    .factory('REST', function($resource){
        return {
            User: $resource('/user/:userId', {'userId': '@user_id'}, {query: {method: 'GET', isArray: false}}),
            Unit: $resource('/unit/:unitNo', {unitNo: '@unit_no'}, {query: {method: 'GET', isArray: false}}),
            Shop: $resource('/shop/:shopNo', {shopNo: '@shop_no'}, {query: {method: 'GET', isArray: false}}),            
            Terminal: $resource('/terminal/:terminalNo', {terminalNo: '@terminal_no'}, {query: {method: 'GET', isArray: false}}),
            Card: $resource('/card/:cardNo', {cardNo: '@card_no'}, {query: {method: 'GET', isArray: false}}),
            CardGroup: $resource('/card/group/:groupId', {groupId: '@group_id'}, {query: {method: 'GET', isArray: false}}),            
            Member: $resource('/member/:memberId', {memberId: '@member_id'}, {query: {method: 'GET', isArray: false}}),
            Role: $resource('/role/:roleNo', {roleNo: '@role_no'}, {query: {method: 'GET', isArray: false}})
        }
    })
    .factory('SMS', function() {
        
    })
;
