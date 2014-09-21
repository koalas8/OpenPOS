'use strict';

/* Directives */


angular.module('angcardApp.directives', [])

	.directive('appVersion', ['version',
		function(version) {
			return function(scope, elm, attrs) {
				elm.text(version);
			};
		}
	])

	.directive('paginator', function() {
		return {
			restrict: 'EA',
			replace: true,
			template: '<ul class="pagination">' +
				'  <li ng-repeat="p in pager.pages"><a href="javascript:;" ng-click="showList(p.page)">{{p.label}}</a></li>' +
				'</ul>',

			link: function(scope, elem, attrs) {

			}
		}
	})

	///////////////////////////////////////////
	// directives for test only
	///////////////////////////////////////////
    
	///////////////////////////////////////////
;