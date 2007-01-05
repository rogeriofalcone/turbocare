var RemoveVendor = function(e){
	replaceChildNodes(e.src().parentNode.parentNode,null);
}
var connectEvent = function() {
	var buttons = getElementsByTagAndClassName('BUTTON',null,'VendorDetails');
	for (j=0; j<buttons.length; j++) {
		connect(buttons[j],'onclick',RemoveVendor);
	}
}
connect(window, 'onload', connectEvent);
