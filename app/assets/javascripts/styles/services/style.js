angular.module('styles.services').factory('Style', function(railsResourceFactory){
	return railsResourceFactory({
		url: 'api/styles', 
		name: 'style'
	});
});