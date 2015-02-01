angular.module('styles.controllers').controller('ListController', function($scope, Style){	
	Style.query().then(function(styles){
		$scope.styles = styles;
	});	
});