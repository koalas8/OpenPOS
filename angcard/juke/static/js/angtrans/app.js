'use strict';


// Declare app level module which depends on filters, and services
angular.module('angtransApp', [
  'ngRoute',
  'angtransApp.filters',
  'angtransApp.services',
  'angtransApp.directives',
  'angtransApp.controllers',
  'ngBootstrap'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/angtrans', {templateUrl: '/static/partials/angtrans/card_trans.html', controller: 'CardTransCtrl'});
  $routeProvider.when('/member', {templateUrl: '/static/partials/angtrans/member.html', controller: 'MemberCtrl'});
  // $routeProvider.otherwise({redirectTo: '/user'});
}]);
