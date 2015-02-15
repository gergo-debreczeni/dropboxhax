/*global angular:false, $scope:false, console:false */
var app = angular.module('dboxApp', []);
 
app.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}]);

app.controller('firstController', ['$scope', '$http', function ($scope, $http) {
    $scope.visible = false;
    $scope.stats = {}
    $scope.button = 'free';
    $scope.showWarning = false;

    $scope.getLocation = function() {
        $scope.showWarning = false;
        if (!$scope.newUrl) {
            $scope.showWarning = true;
            return;
        }
        var l = document.createElement("a");

        l.href = $scope.newUrl;
        // return l;
    };

    $scope.isActive = function(route) {
        return route === $location.path();
    }

}]);

