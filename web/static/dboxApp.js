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

    $scope.getUrlElement = function(url) {
        var l = document.createElement("a");
        l.href = url;
        return l;
    };

    $scope.isActive = function(route) {
        return route === $location.path();
    }

    $scope.getLocation = function(){
        $scope.showWarning = false;
        $scope.showBadUrlWarning = false;

        if (!$scope.newUrl) {
            $scope.showWarning = true;
            return;
        }
        
        var obj = JSON.parse('{"url": "' + $scope.newUrl +'", "offer": "' + $scope.button + '"}');
        console.log(obj);
        console.log(obj);

        $http({
            method: "post",
            url: "/add_url",
            headers: {'Content-Type': "application/json"},
            data: obj
        }).success(function (response) {
            if (response=="invalidUrl"){
                $scope.showBadUrlWarning = true;
                return;
            }
        });

    };

}]);

