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
	// Clone the non-draggable items
	var FirstClones = new Array();
       var d = getElementsByTagAndClassName('DIV', 'rowdisplay',Drag._parent);
        for (var i=0;i<d.length;i++){
		var clone = d[i].parentNode.cloneNode(true);
		FirstClones[i] = clone;
	}
	var SecondClones = new Array();
	var d1 = getElementsByTagAndClassName('DIV', 'loadsubtables',Drag._parent);
	for (var i=0;i<d1.length;i++){
		var clone = d1[i].parentNode.cloneNode(true);
		SecondClones[i] = clone;
	}
	var ThirdClones = new Array();
	var d1 = getElementsByTagAndClassName('DIV', 'removetable',Drag._parent);
	for (var i=0;i<d1.length;i++){
		var clone = d1[i].parentNode.cloneNode(true);
		ThirdClones[i] = clone;
	}
	// Clone all the inputs for the table item
	var InputClones = new Array();
	var Inputs = getElementsByTagAndClassName('INPUT',null,Drag._parent);
	var inputcount = 0;
	for (var i=0;i<Inputs.length;i++) {
		if (Drag._parent.id == Inputs[i].parentNode.id) { //Make sure the node is a child node and not a child child node
			var clone = Inputs[i].cloneNode(true);
			InputClones[inputcount] = clone;
			inputcount++;
		}
	}
	// Replace all the draggable items
	replaceChildNodes(Drag._parent,null);
	// Re-Add non draggable items
	for (var i=0;i<FirstClones.length;i++){
		Drag._parent.appendChild(FirstClones[i]);
	}	
	for (var i=0;i<SecondClones.length;i++){
		Drag._parent.appendChild(SecondClones[i]);
	}	
	for (var i=0;i<ThirdClones.length;i++){
		Drag._parent.appendChild(ThirdClones[i]);
	}	
	// Re-Add draggable items
	for (var i=0;i<clones.length;i++){
		Drag._parent.appendChild(clones[i]);
	}
	// Re-Add input items
	for (var i=0;i<InputClones.length;i++){
		Drag._parent.appendChild(InputClones[i]);
	}
	// reconnect the drag event
       var d = getElementsByTagAndClassName('DIV', 'draggable',Drag._parent);
       for (var i=0;i<d.length;i++){
		connect(d[i], 'onmousedown', Drag.start);
	}
	//  reconnect the column display event
        var d = getElementsByTagAndClassName('DIV', 'displayable',Drag._parent);
        forEach(d,
            function(elem) {
                connect(elem, 'onclick', ColDisplay.toggle);
            });
	//  reconnect the row display event
        var d = getElementsByTagAndClassName('DIV', 'rowdisplay',Drag._parent);
        forEach(d,
            function(elem) {
                connect(elem, 'onclick', RowDisplay.toggle);
            });
		var loadsubtables = getElementsByTagAndClassName('DIV',"loadsubtables",Drag._parent);
		for (i=0;i<loadsubtables.length; i++){
			connect(loadsubtables[i],"onclick",qry.LoadSubTables);
		}
		var removetable = getElementsByTagAndClassName('DIV',"removetable",Drag._parent);
		for (i=0;i<removetable.length; i++){
			connect(removetable[i],"onclick",qry.RemoveTable);
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
    
/*

	Toggle a Div to a different colour to indicate that it is not displayed or displayed
	This is for a column

*/
ColDisplay = {

    toggle: function(e) {
        e.stop();
        ColDisplay._target = e.src().parentNode;
        /*
            Toggle the displaying of rows
        */
	if (hasElementClass(ColDisplay._target,'mark-hidden')) {
		removeElementClass(ColDisplay._target,'mark-hidden');
		addElementClass(ColDisplay._target,'mark-shown');
	} else {
		removeElementClass(ColDisplay._target,'mark-shown');
		addElementClass(ColDisplay._target,'mark-hidden');
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
                connect(elem, 'onclick', ColDisplay.toggle);
            });
                        
    });
    
/*

	Toggle a row to hide/show

*/
RowDisplay = {

    toggle: function(e) {
        e.stop();
       RowDisplay._target = e.src().parentNode.parentNode;
        var d = getElementsByTagAndClassName('DIV', 'tablecol',RowDisplay._target);
	// set the display on all the columns
	for (i=0;i<d.length;i++){
		if (hasElementClass(d[i],'hide-row')) {
			removeElementClass(d[i],'hide-row');
			addElementClass(d[i],'show-row');
		} else {
			removeElementClass(d[i],'show-row');
			addElementClass(d[i],'hide-row');
		}
	}
	// set the display on the entire table
	if (hasElementClass(RowDisplay._target,'hide-row')) {
		removeElementClass(RowDisplay._target,'hide-row');
		addElementClass(RowDisplay._target,'show-row');
	} else {
		removeElementClass(RowDisplay._target,'show-row');
		addElementClass(RowDisplay._target,'hide-row');
	}
    }
};

connect(window, 'onload',   
    function() {
        /*
            Find all DIVs tagged with the displayable class, and connect them to
            the Display handler.
        */
        var d = getElementsByTagAndClassName('DIV', 'rowdisplay');
        forEach(d,
            function(elem) {
                connect(elem, 'onclick', RowDisplay.toggle);
            });
                        
    });