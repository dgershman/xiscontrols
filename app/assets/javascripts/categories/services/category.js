angular.module('categories.services').factory('Category', function(railsResourceFactory){
	return railsResourceFactory({
		url: 'api/categories', 
		name: 'category'
	});
});