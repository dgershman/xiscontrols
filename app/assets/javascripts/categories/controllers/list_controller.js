angular.module('categories.controllers').controller('ListController', function($scope, Category){	
	Category.query().then(function(categories){
		$scope.categories = categories;
	});	
});