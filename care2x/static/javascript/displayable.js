/*

	Toggle a Div to a different colour to indicate that it is not displayed or displayed

*/
Display = {

    toggle: function(e) {
        e.stop();
        Display._target = e.src().parentNode;
        /*
            There's no cross-browser way to get offsetX and offsetY, so we
            have to do it ourselves. For performance, we do this once and
            cache it.
        */
	if (hasElementClass(Display._target,'mark-hidden')) {
		removeElementClass(Display._target,'mark-hidden');
		addElementClass(Display._target,'mark-shown');
	} else {
		removeElementClass(Display._target,'mark-shown');
		addElementClass(Display._target,'mark-hidden');
	}
    }
};

connect(window, 'onload',   
    function() {
        /*
            Find all DIVs tagged with the displayable class, and connect them to
            the Display handler.
        */
        var d = getElementsByTagAndClassName('DIV', 'displayable');
        forEach(d,
            function(elem) {
                connect(elem, 'onclick', Display.toggle);
            });
                        
    });