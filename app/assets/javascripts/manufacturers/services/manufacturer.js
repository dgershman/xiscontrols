angular.module('manufacturers.services').factory('Manufacturer', function(railsResourceFactory){
	return railsResourceFactory({
		url: 'api/manufacturers', 
		name: 'manufacturer'
	});
});