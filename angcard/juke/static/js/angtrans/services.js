'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('angtransApp.services', ['ngResource'])
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
                        data: jQuery.toJSON(data),                        
                    }).success(function(data){
                        alert(data.msg);
                        return data.success;                        
                    });
                }
            }    
        };
    }])
    .factory('Store',function ($resource) {
        return {
            city: $resource('/city'), 
            memberLevel: $resource('/member/level'),
            member: $resource('/member'),       

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
        return function(fetchFunction, pageSize){
            var paginator = {
                hasNextVar: false,
                next: function(){
                    if (this.hasNextVar){
                        this.currentOffset += pageSize;
                        this._load();
                    }
                },
                _load: function(){
                    var self = this;
                    fetchFunction(this.currentOffset, pageSize + 1, function(items){
                        self.currentPageItems = items.slice(0, pageSize);
                        self.hasNextVar = items.length === pageSize + 1;
                    });
                },
                hasNext: function(){
                    return this.hasNextVar;
                },
                previous: function(){
                    if(this.hasPrevious()){
                        this.currentOffset -= pageSize;
                        this._load();
                    }
                },
                hasPrevious: function(){
                    return this.currentOffset !== 0;
                },
                currentPageItems: [],
                currentOffset: 0
            };
            // Load the 1st page
            paginator._load();
            return paginator;
        };
    })
;
