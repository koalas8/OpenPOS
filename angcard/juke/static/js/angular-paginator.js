(function() {
	'use strict';

	angular.module('jukePager', [])
		.directive('jukePagination', function() {
			return {
				 restrict: 'E'
				scope: {
					url: '=',
					dataStore: '=',
					jumps: '=?'
				},
				templateUrl: function(element, attr) {
					return attr.templateUrl;
				},
				replace: true,
				controller: ['$scope', '$http', function($scope, $http) {
					$scope.reloadPage = false;
					$scope.paginated = false;				

					function request(page, limit) {
						$http.get($scope.url, {params: {page: page, limit: limit}})
							 .success(function(resp) {
							 	$scope.dataStore = resp;
							 	$scope.totalRow = resp.total;
							 	$scope.perPage = resp.limit;
							 	$scope.currentPage = 1;
							 });
					};

					$scope.getPageGroup = function() {		
						var _jumps = typeof($scope.jumps) === 'number' ? parseInt($scope.jumps) : 10;  // 每页显示10个跳转
						var _total = $scope.totalRow;
						var _limit = $scope.perPage;
			            var _totalPage = _total % _limit == 0? parseInt(_total/_limit): parseInt(_total/_limit) + 1;  // 共多少页
			            var _startPage;
			            var _endPage;
			            if (jumps >= _totalPage) {
			                _startPage = 1;
			                _endPage = _totalPage;
			            } else {
			                _startPage = page - parseInt(jumps/2);
			                _startPage = _startPage < 1 ? 1 : _startPage;
			                _endPage = _startPage + jumps - 1;
			                _endPage = _endPage > _totalPage ? _totalPage : _endPage;
			            }
			                  
			            var pages = [];
			            for(var i=_startPage; i<=_endPage; i++){
			                pages.push({page: i, 'label': i});
			            }
			            return pages;
					}

					$scope.gotoPage = function(page){
						// 不能超出前后范围
						if(page < 0 || (page-1)*$scope.perPage > $scope.totalRow){
							return;
						}

						request(page, $scope.perPage);
					};

					$scope.$watch('currentPage', function(newPage, oldPage) {
						if(newPage !== oldPage) {
							$scope.gotoPage(newPage);
						}
					});

					$scope.$watch('url', function(newUrl, oldUrl) {
						if (newUrl !== oldUrl) {
							alert('abc');
							$scope.gotoPage(1);
						}
					});
				}]
			}
		})
}());