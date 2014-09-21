(function() {
	'use strict';
	angular.module('jukeColorPicker', [])
		.directive('jukeColorPicker', function() {
			return {
				restrict: 'A',
				require: '?ngModel',
				link: function(scope, element, attrs) {
					// $(element).pickAColor({
					//   showSpectrum            	: true,
					// 	showSavedColors         : true,
					// 	saveColorsPerElement    : true,
					// 	fadeMenuToggle          : true,
					// 	showAdvanced			: true,
					// 	showBasicColors         : true,
					// 	showHexInput            : true,
					// 	allowBlank				: true,
					// 	inlineDropdown			: true
					// });
				}
			}
		});
})();