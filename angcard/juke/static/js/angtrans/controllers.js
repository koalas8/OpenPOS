'use strict';

/* Controllers */

angular.module('angtransApp.controllers', []).


    controller('CardTransCtrl', ['$scope', '$http', function ($scope, $http) {

        $scope.trans = {trans_code: '000010'}; // 默认消费交易

        $scope.setTransCode = function(trans_code){
            $scope.trans.trans_code = trans_code;            
        }

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
            }       
            return trans_dim['code_' + $scope.trans.trans_code]
        }

        $scope.show = function(input){
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
            return $.inArray(input, ctrl) >= 0? true: false;
        }

        $scope.setTrack2 = function(track2) {
            track2 = track2.trim();
            if (track2.length == 37) {
                $scope.trans.card_no = track2.substr(0, 18);                
                $scope.trans.track_2 = track2;
                alert($scope.trans.card_no);
            }
        }

        $scope._print = function(print_content) {
            var LODOP=getLodop(document.getElementById('LODOP_OB'),document.getElementById('LODOP_EM')); 
            if((LODOP!=null)&&(typeof(LODOP.VERSION)!="undefined")){
                // 打印
                //LODOP.ADD_PRINT_HTM(0, 0, '100%', '100%', document.getElementById('ticket').innerHTML);
                LODOP.ADD_PRINT_TEXT('5mm', '3mm', '58mm', '80mm', print_content);
                LODOP.SET_PRINT_PAGESIZE(3, '58mm', '2mm', 'CreateCustomPage');
                //LODOP.PREVIEW();
                LODOP.PRINT();
            }else{
                alert('未安装打印控件，小票不能打印');
            }
        }

        $scope.doTrans = function(transForm) {
            $http.post('/webtrans', $scope.trans)
            .success(function(data){
              if (data.success) {
                $scope._print(data.data.print_text);
              }
            });
        }
    }])

    .controller('MemberCtrl', ['$scope', '$http', function ($scope, $http) {
        // 当前状态
        $scope.menu = {action: 'list'};
        // 为form提供数据
        $scope.memberForm = {action: 'add'};
        // 获取城市信息
        $http.get('/city').success(function(data){
            $scope.memberForm.provinces = data.data;
        });
        // 获取会员等级信息
        $http.get('/member/level').success(function(data){
            $scope.memberForm.level = data.data;
        });

        // 添加或修改时的member信息
        $scope.member = {};

        // 添加或更新会员信息的函数
        $scope.addOrUpdate = function(member){
            if ($scope.memberForm.action == 'add'){
                $http.post('/member', $scope.member).success(function(data){
                    alert(data.msg);
                    if(data.success){
                        $scope.member = {};
                    }
                });
            } else {
                $http.put('/member', $scope.member).success(function(data){
                    alert(data.msg);
                    if (data.success){
                        $scope.member = {};
                    }
                });
            }
        }
        
        $scope.getCities = function(pid, level){      
            // 地址的级联菜单
            // level: 菜单的级别, 1-城市 2-区县 3-街道/村镇      
            $http.get('/city', {params: {pid: pid}}).success(function(data){
                if (!data.success){
                    alert(data.msg);
                    return;
                }
                switch(level){
                    case 1: $scope.memberForm.cities = data.data; break;
                    case 2: $scope.memberForm.districtes = data.data; break;
                    case 3: $scope.memberForm.countries = data.data; break;
                }
            });
        }

        $scope.getMembers = function(keyword){
            $http.get('/member/list', {keyword: keyword}).success(function(data){
                if (!data.success){
                    alert(data.msg);
                    return;
                }
                $scope.memberStore = data;
            });
        }
        $scope.getMembers();

        $scope.setAction = function(action){
            $scope.menu.action = action;
        }

    }])