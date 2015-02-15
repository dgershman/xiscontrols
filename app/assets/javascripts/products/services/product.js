angular.module('products.services').factory('Product', function(railsResourceFactory){
	return railsResourceFactory({
		url: 'api/products', 
		name: 'product'
	});
});