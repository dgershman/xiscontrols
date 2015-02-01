angular.module('manufacturers.controllers').controller('ListController', function($scope, Manufacturer){	
	Manufacturer.query().then(function(manufacturers){
		$scope.manufacturers = manufacturers;
	});	
});