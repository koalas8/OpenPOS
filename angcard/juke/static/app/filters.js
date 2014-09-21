'use strict';

/* Filters */

angular.module('angcardApp.filters', [])
    .filter('interpolate', ['version', function (version) {
        return function (text) {
            return String(text).replace(/\%VERSION\%/mg, version);
        }
    }])
    .filter('statusToHanZi', function () {
        var _filter = function (status) {
            var hanZi = '';
            switch (status) {
                case '0':
                    hanZi = '正常';
                    break;
                case '1':
                    hanZi = '已禁用';
                    break;
            }
            return hanZi;
        }
        return _filter;
    })
    .filter('cardStatusToHanZi', function () {
        var _filter = function (status) {
            var hanZi = '';
            switch (status) {
                case '0':
                    hanZi = '正常';
                    break;
                case '1':
                    hanZi = '新卡未启用';
                    break;
                case '3':
                    hanZi = '冻结';
                    break;
                default:
                    hanZi = status;
            }
            return hanZi;
        }
        return _filter;
    })
    .filter('orgLevel', function () {
        var _filter = function (level) {
            var levelName = '';
            switch (level) {
                case 'super':
                    levelName = '超级用户';
                    break;
                case 'unit':
                    levelName = '集团级用户';
                    break;
                case 'shop':
                    levelName = '商户级用户';
                    break;
                case 'terminal':
                    levelName = '终端操作员'
                    break;
            }
            return levelName;
        }
        return _filter;
    })
    .filter('yesOrNoFilter', function () {
        var _filter = function (trueOrFalse) {
            if (trueOrFalse == true) {
                return '是';
            } else if (trueOrFalse == false) {
                return '否';
            } else {
                return '未知';
            }
        }
        return _filter;
    })
    .filter('modeOfPaymentFilter', function () {
        var _filter = function (mode) {
            if (mode == 'card') {
                return '卡支付';
            } else if (mode == 'cash') {
                return '现金支付';
            } else if (mode == 'mixed') {
                return '联合支付'
            } else {
                return '未知';
            }
        }
        return _filter;
    })
    .filter('cnyuan', function () {
        var _filter = function (value) {
            return '￥' + value;
        }
        return _filter;
    })
    .filter('unitTypeFilter', function(){
        var _filter = function (type) {
            var typeName = '';
            switch (type) {
                case '0':
                    return '免费用户';
                    break;
                case '1':
                    return '付费用户';
                    break;
            }
            return typeName;
        }
        return _filter;
    });
