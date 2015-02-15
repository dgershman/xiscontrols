angular.module('products.controllers').controller('ListController', function($scope, Product){	
	Product.query().then(function(products){
		$scope.products = products;
	});	
});