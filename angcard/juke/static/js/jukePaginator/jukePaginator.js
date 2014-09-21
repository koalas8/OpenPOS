(function() {
	'use strict';
	angular.module('jukePaginate', [])
		.directive('jukePagination', function() {			
			return {
				restrict: 'E',
				scope: {
					url: '=',
					collection: '=',
					templateUrl: '=',
					query: '=?',
					page: '=?',
					limit: '=?',
					jumps: '=?'
				},
				templateUrl: function(element, attr) {
                    if(!attr.templateurl){
                        return '/static/js/jukePaginator/template.html';
                    }
					return attr.templateurl;
				},
				replace: true,
				controller: ['$scope', '$http', function($scope, $http) {	
					$scope.page = $scope.page == undefined ? 1 : parseInt($scope.page);
					$scope.limit = $scope.limit == undefined ? 10 : parseInt($scope.limit);
					$scope.jumps = $scope.jumps == undefined ? 10 : parseInt($scope.jumps);
                    $scope.pageBar = {first: 1, last: 1, current: 1, pages: []};
					// 请求当前页的数据
					function requestData() {
						if ($scope.url == undefined) {
							return;
						}

						$http.get(
							$scope.url, 
							{params: {page: $scope.page, limit: $scope.limit}}
							).success(function(resp) {
								$scope.collection = resp;
								$scope.page = resp.page;
								$scope.limit = resp.limit;

                                var pages = 0;  // 共有多少页面
                                var last = 1;  // 最后一页的页码
                                var total = $scope.collection.total || 0;
                                var limit = $scope.collection.limit || 10;

                                if(total % limit > 0) {
                                    pages = Math.floor(total / limit) + 1;
                                } else {
                                    pages = total / limit;
                                }

                                last = pages <= 0 ? 1 : pages;  // 设置跳转到最后一页

                                var minPage = 1;
                                var maxPage = $scope.jumps;
                                if($scope.page > $scope.jumps) {  // 当前页面的值大于跳转的值，将当前页放中间
                                    minPage = $scope.page - Math.floor($scope.jumps/2);
                                    maxPage = minPage + $scope.jumps - 1;
                                } else {
                                    maxPage = pages;
                                }

                                $scope.pageBar.current = $scope.page;
                                $scope.pageBar.last = last;
                                $scope.pageBar.pages = [];
                                for (var i=minPage; i<=maxPage; i++) {
                                    $scope.pageBar.pages.push(i);
                                }
							});
					}
                    requestData();
					$scope.gotoPage = function(page) {
						console.log('gotoPage(' + page + ')');
						page = page == undefined ? 1 : page;
						// 不能超出前后范围
						var limit = $scope.collection == undefined ? 10 : $scope.collection.limit;
						var total = $scope.collection == undefined ? 10 : $scope.collection.total;
						if (page < 0 || (page-1)*limit > total){
							return;
						}
						$scope.page = page;
						requestData();
					}

					// 监视url属性变化
					$scope.$watch('url', function(newUrl, oldUrl) {
						if(newUrl == oldUrl) return;
                        if(!newUrl) return;
						requestData();
					});
				}]
			}
		})
}());