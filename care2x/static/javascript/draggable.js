/*

    Drag: A Really Simple Drag Handler
    Originally from the Mochikit web-site, but hacked by Wes for the TurboCare project
    
    The original used absolute coordinates.  This is a little more complicated since it will
    try to reposition a DOM object in the DOM tree based on where it is dragged on the 
    screen
    
*/
Drag = {
    _move: null,
    _down: null,
    _parent: null,
    
    start: function(e) {
        e.stop();
        // We need to remember what we're dragging.
        Drag._target = e.src().parentNode;
	Drag._parent = e.src().parentNode.parentNode;
        /*
            There's no cross-browser way to get offsetX and offsetY, so we
            have to do it ourselves. For performance, we do this once and
            cache it.
        */
        Drag._offset = Drag._diff(e.mouse().page, elementPosition(e.target()));
	//Drag._offset = elementPosition(Drag._target);
        //Drag._offset = elementPosition(e.mouse().page);
        Drag._move = connect(document, 'onmousemove', Drag._drag);
        Drag._down = connect(document, 'onmouseup', Drag._stop);
	// Change the element from relative position to absolute
	Drag._target.style.position = "absolute";
    },

    _offset: null,
    _target: null,
    
    _diff: function(lhs, rhs) {
        return new MochiKit.DOM.Coordinates(lhs.x - rhs.x, lhs.y - rhs.y);
    },
        
    _drag: function(e) {
        e.stop();
        setElementPosition(Drag._target,Drag._diff(e.mouse().page, Drag._offset));
    },
    
    _stop: function(e) {
        disconnect(Drag._move);
        disconnect(Drag._down);
	var NodeNumber = Drag._swap_with(elementPosition(Drag._target).x);
	//Clone all the nodes
       var d = getElementsByTagAndClassName('DIV', 'draggable',Drag._parent);
       var clones = new Array(d.length);
       var arr_i = 0;
       var isInsert = false;
        for (i=0;i<d.length;i++){
		if ((i==NodeNumber)&&(!isInsert)) {
 			var clone = Drag._target.cloneNode(true);
			clone.style.position = "relative";
			clone.style.left = "0px";
			clone.style.top = "0px";
			clones[arr_i] = clone;
			arr_i++;
			i--;
			isInsert = true;
		} else if (d[i].parentNode.id != Drag._target.id) {
			var clone = d[i].parentNode.cloneNode(true);
			clones[arr_i] = clone;
			arr_i++;
		}
	}
	replaceChildNodes(Drag._parent,null);
	for (i=0;i<clones.length;i++){
		Drag._parent.appendChild(clones[i]);
	}
	// reconnect the drag event
       var d = getElementsByTagAndClassName('DIV', 'draggable',Drag._parent);
       for (i=0;i<d.length;i++){
		connect(d[i], 'onmousedown', Drag.start);
	}
    },
    
    _swap_with: function(x) {
	//Get all the draggables from the parent
        var d = getElementsByTagAndClassName('DIV', 'draggable',Drag._parent);
        for (i=0;i<d.length;i++){
		var pos = elementPosition(d[i].parentNode);
		if (pos!=null){
			var dim = elementDimensions(d[i].parentNode);
			if ((((i==0) && (x<=pos.x))|| ((x >= pos.x) && (x <= (pos.x + dim.w))) || ((i==d.length-1) && (x <= pos.x)))&&
			    (Drag._target.id!=d[i].parentNode.id)){
				//alert(i);
				return i;
			}
		}
	}
	return 0;
    }
};

connect(window, 'onload',   
    function() {
        /*
            Find all DIVs tagged with the draggable class, and connect them to
            the Drag handler.
        */
        var d = getElementsByTagAndClassName('DIV', 'draggable');
        forEach(d,
            function(elem) {
                connect(elem, 'onmousedown', Drag.start);
            });
                        
    });