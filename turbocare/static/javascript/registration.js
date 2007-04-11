//Document wide variables
var barcode = {};//The barcode object
//The barcode value
barcode.CustomerID = ''; //Defined as 20 numeric characters followed by a enter key
barcode.PatientID = '';//Defined as 18 numeric characters followed by a enter key
//capture the keypress event.  We're looking for 20 consecutive numeric values
//followed by an enter key.  The enter key is captured by a separate function.
barcode.keypress = function(dom_obj){
	if (dom_obj.modifier()['any'] == false){
		var key = dom_obj.key()['string'];
		if (isNaN(key)) {
			barcode.CustomerID = '';
			barcode.PatientID = '';
		} else {
			barcode.CustomerID = barcode.CustomerID + key;
			barcode.PatientID = barcode.PatientID + key;
		}
		if (barcode.CustomerID.length > 20) {
			barcode.CustomerID = '';
		}
		if (barcode.PatientID.length > 18) {
			barcode.PatientID = '';
		}
	} else {
		barcode.CustomerID = '';
		barcode.PatientID = '';
	}
}
//Capture the enter key.  If our barcode is full when an enter key is pressed
//We are most likely entering a barcode.  At this point, we signal a barcode event!
barcode.keydown = function(dom_obj) {
	if ((dom_obj.key()['string']=='KEY_ENTER') && (barcode.CustomerID.length==20)){
		//alert(barcode.CustomerID);
		signal(document,'customerid',barcode.CustomerID);
	} else if ((dom_obj.key()['string']=='KEY_ENTER') && (barcode.PatientID.length==18)){
		//alert(barcode.PatientID);
		signal(document,'patientid',barcode.PatientID);
	} else if (dom_obj.key()['string']=='KEY_ENTER') {
		barcode.CustomerID = '';
		barcode.PatientID = '';
	}
}
/*
	Events for the barcode reader.  The connect operations are made at the bottom of the document
*/
//When a customerid event (custom event) is fired, we process it here
barcode.LoadCustomerID = function(dom_obj) {
	//Load the items available for the customer
  	var postVars = 'CustomerID='+barcode.CustomerID;
	barcode.CustomerID = '';
	document.location.href = 'RegistrationPage1?'+postVars;
}
//When a PatientID event (custom event) is fired, we process it here
barcode.LoadPatientID = function(dom_obj) {
	//Load the items available for the customer
  	var postVars = 'PatientID='+barcode.PatientID;
	barcode.PatientID = '';
	document.location.href = 'RegistrationPage1?'+postVars;
}


/*
	My custom shortcuts:
	1. Open a dialog box for entering a customer id
*/
var shortcuts = {};//keyboard short cut operations
shortcuts.keypress = function(dom_obj){
	if ((dom_obj.modifier()['ctrl'] == true) && (dom_obj.key()['string'] == 'l')) {
		dom_obj.stop();
		reg.renderCustomerIdDialog();
	}
}
shortcuts.keydown = function(dom_obj){
	if (dom_obj.key()['string']=='KEY_ENTER') {
		var el = dom_obj.target();
		//Perform a search
		if (el.id == 'dialog_CustomerID' && !isNaN(el.value)) {
			var postVars = 'CustomerID='+el.value;
			document.location.href = 'RegistrationPage1?'+postVars;			
		}
	}
}

//AJAX Post function
function postJSON(url, postVars) {
	reg.toggle_message("Sending request...");
    var req = getXMLHttpRequest();
    req.open("POST", url, true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  	var data = postVars; 
    var d = sendXMLHttpRequest(req, data);
    return d.addCallback(evalJSONRequest);
}

//Funky redraw function
function redraw(){
	resizeBy(-1,0);
	resizeBy(1,0);
}

var reg = {};


// variables ===================
reg.g_nTimeoutId;
reg.CustomerId = '';
reg.DateBirth = '';
reg.Age = '';
reg.ContactName = '';
reg.ContactID = '';
// utility functions ===========

/*
	When someone enters an age, modify the DateBirth
	entry to match the age to the date.
*/
reg.AgePickUpdate = function(dom_obj){
	var Age = getElement('Age').value;
	if (Age == '') {
		return false;
	} else if (isNaN(Age)){
		getElement('Age').value = '';
	} else if (Age != reg.Age) {
		var Today = new Date();
		var DateBirth = new Date(Today.getFullYear() - Age, Today.getMonth(), Today.getDate());
		getElement('DateBirth').value = toISODate(DateBirth);
		reg.Age = Age;
		reg.DateBirth = toISODate(DateBirth);
	}
}
/*
	When someone modifies PatientType, show/hide the Insurance Information
	If Private Insurance, then show Insurance Information, otherwise, hide
*/
reg.PatientTypeOnChange = function(evt_obj){
	if (scrapeText('PatientType',true)[getElement('PatientType').value] == 'Private Insurance') {
		getElement("rowInsuranceProvider").style.display = '';
		getElement("rowInsuranceNumber").style.display = '';		
	} else {
		getElement("rowInsuranceProvider").style.display = 'None';
		getElement("rowInsuranceNumber").style.display = 'None';		
	}
}
/*
	Open a date entry javascript box
*/
reg.DatePick = function(dom_obj){
	if ((dom_obj.type() == 'click') || (dom_obj.type()=='keydown' && (dom_obj.key()['string']=='KEY_ARROW_DOWN'))) {
		if (dom_obj.type() == 'keydown') {
			dom_obj.stop();
		}
		Widget.pickDateTime("DateBirth");
	}
}
/*
	When a date has been entered, update
	the age box
*/
reg.DatePickUpdate = function(dom_obj){
	var DateBirth = isoDate((getElement("DateBirth").value).slice(0,10));
	getElement('DateBirth').value = toISODate(DateBirth);
	if (getElement('DateBirth').value != reg.DateBirth) {
		var Today = new Date();
		var diff = Today.getTime() - DateBirth.getTime();
		getElement('Age').value = parseInt((diff + 43200000)/(31557600000));
		reg.Age = getElement('Age').value;
		reg.DateBirth = toISODate(DateBirth);
	}
}
/*
	Ward OnChange: for page 3 of registration, when someone changes the ward
	then we have to load the available rooms for that ward
*/
reg.WardOnChange = function(dom_obj){
	reg.toggle_message("Searching...");
	var postVars = 'WardID=' + getElement('Ward').value;
	var d = postJSON('RegistrationRooms',postVars);
	d.addCallbacks(reg.RenderRooms,reg.error_report);
}
/*
	Room OnChange: for page 3 of registration, when someone changes the room
	then we have to load the available beds for that room
*/
reg.RoomOnChange = function(dom_obj){
	reg.toggle_message("Searching...");
	var postVars = 'WardID='+getElement('Ward').value+'&RoomNr=' + getElement('Room').value+'&EncounterID='+getElement('EncounterID').value;
	var d = postJSON('RegistrationBedsInRoom',postVars);
	d.addCallbacks(reg.RenderBeds,reg.error_report);
}

reg.collectPostVars = function(f){
  var postVars='';
  for(var i=0; i<f.elements.length;i++)
  {
    var t = f.elements[i].type;
    if(t.indexOf('text') > -1 )
    {
      if(postVars!='') postVars+='&';
      postVars+= f.elements[i].name +'='+ encodeURIComponent(f.elements[i].value);
    }
    if(t.indexOf('hidden') > -1 )
    {
      if(postVars!='') postVars+='&';
      postVars+= f.elements[i].name +'='+ encodeURIComponent(f.elements[i].value);
    }
    if(t.indexOf('select') > -1)
    {
      if(postVars!='') postVars+='&';
      if (getNodeAttribute(f.elements[i],'multiple') != null) {
      	postVars+= f.elements[i].name +'='+ encodeURIComponent(reg.multiselect_csv(f.elements[i].id));
      } else {
      	postVars+= f.elements[i].name +'='+ encodeURIComponent(f.elements[i].options[f.elements[i].selectedIndex].value);
      }
    }
  }
  return postVars;
}

reg.multiselect_csv = function(element_id){
	var nodes = getElement(element_id).childNodes;
	var csv = '';
	for (var i=0;i<nodes.length;i++){
	 	if (nodes[i].selected){
	 		csv += nodes[i].value +',';
	 	}
	}
	csv = csv.slice(0,csv.length-1);
	return csv;
}

reg.clearAllFormFields = function(parentid){
	elems = getElementsByTagAndClassName('input',null,parentid);
	for (var i=0;i<elems.length;i++){
		elems[i].value = "";
	}
}

// AJSON reactions ==================
reg.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	reg.toggle_message("");
	if (data.result_msg != null) {
		var display = createDOM('DIV',{'class':'displaymsg','id':'last_result_msg'},data.result_msg);
		if (getNodeAttribute('last_result_msg','class') == null){
			document.body.appendChild(display);
		} else {
			swapDOM(field.id,display);
		}
	}
	var d = callLater(5,remove_message);
}
reg.error_report = function(data){
	reg.toggle_message("ERROR");
	var d = callLater(5,reg.toggle_message);
}

reg.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

reg.merge_hidden_inputs = function(parentid){
//Take all inputs under the parent and for any hidden input with a visible input having the same name
//Copy the value to the visible input and remove the hidden input from DOM
	var inputs = getElementsByTagAndClassName('INPUT',null,parentid);
	for (i=0;i<inputs.length;i++){
		if (getNodeAttribute(inputs[i],'type') == 'hidden') {
			for (j=0;j<inputs.length;j++){
				if (getNodeAttribute(inputs[i],'name') == getNodeAttribute(inputs[j],'name') && (getNodeAttribute(inputs[j],'type')!='hidden')) {
					//copy the value from the hidden field to the visible field
					inputs[j].value = inputs[i].value;
					//change the name of the hidden field
					inputs[i].name = inputs[i].name + '_remove';
				}
			}
		}
	}
}
// AJSON actions ====================


/*
	Call the search procedure and return the results below
*/
reg.CityTownSearchKeyDown = function(dom_obj){
	if (dom_obj.key()['string']=='KEY_ENTER') {
		var Input = dom_obj.src();
		dom_obj.stop();
		reg.toggle_message("Searching...");
		var postVars = Input.name + '=' + Input.value;
		var d = postJSON('RegistrationCityTownSearch',postVars);
		d.addCallbacks(reg.RenderCityTownSearch,reg.error_report);
	}
}

/*
	There are two parameters: customer_id and receipt_id, which are two
	DIVs which might contain numbers.  If they do, then we want to load
	them when the page finishes loading.  Otherwise, do nothing.
*/
reg.OpenOnLoad = function() {
	if (getElement('PatientType')!=null) {
		getElement('PatientType').focus();
	} else if (getElement('ContactPerson')!=null) {
		getElement('ContactPerson').focus();
	}
}

/*
	AJSON Reactions to the above actions
*/

/* 	Render the AddressCityTown search screen
	This is just the main part of the box, not the 
	search results
*/
reg.RenderCityTownSearch = function(data){
	var Input = function(name, value, label) {
		if (label == null) {
			label = name;
		}
		if (value == null) {
			value = '';
		}
		var row = createDOM('DIV',{'id':'row_cts_'+name, 'class':'row'});
		var title = createDOM('DIV',null,label);
		var input = createDOM('INPUT',{'id':'cts_'+name,'type':'text','name':name,'value':value}); //cts: city town search
		var data = createDOM('DIV',null);
		data.appendChild(input);
		appendChildNodes(row,title,data);
		return row;
	}
	//Reset the message
	reg.toggle_message("");
	//Remove any existing search box
	if (getNodeAttribute('CityTownSearchBox','class') == 'dialogbox') {
		reg.CloseCityTownSearch();
	}
	var dialog = createDOM('DIV',{'style':'height:400px; width:400px', 'id':'CityTownSearchBox','class':'dialogbox'});
	var shadow = createDOM('DIV',{'id':'CityTownSearchBoxShadow','style':'height:410px;width:410px','class':'dialogbox_shadow'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:reg.CloseCityTownSearch()'},"Close");
	dialog.appendChild(close_link);
	//The main table
	var table = createDOM('DIV',{'id':'CityTownSearchTable','class':'divtable_input'});
	// Add fields
	var firstrow = Input('CityTownName',data.city_town_name,'City name');
	table.appendChild(firstrow);
	table.appendChild(Input('Block',data.block));
	table.appendChild(Input('District',data.district));
	table.appendChild(Input('PostOffice',data.post_office));
	table.appendChild(Input('State',data.state));
	table.appendChild(Input('Country',data.country));
	//Add button
	table.appendChild(createDOM('INPUT',{'id':'btnCityTownSearch','type':'BUTTON','value':'Search'}));
	//Create our dialog
	dialog.appendChild(table);
	document.body.appendChild(shadow);
	setOpacity(shadow,0.5);
	document.body.appendChild(dialog);
	//Add a place for the Search results
	dialog.appendChild(createDOM('DIV',{'id':'CityTownSearchResults','style':'overflow:auto;height:180px;font-size:11px;width:390px;list-style-type: none','class':'ListItemRow'},'Press Search'));
	//Attach our button event
	connect('btnCityTownSearch','onclick',reg.CityTownSearchUpdate);
	//Attach our Enter event
	var Inputs = getElementsByTagAndClassName('INPUT',null,table);
	for (i=0; i<Inputs.length; i++) {
		if (getNodeAttribute(Inputs[i],'type')=='text') {
			connect(Inputs[i],'onkeydown',reg.CityTownSearchUpdateKeyDown);
		}
	}
	//connect the dialog box to another event handler for up/down arrow keys and enter key press outside the fields
	connect(dialog,'onkeydown',reg.CityTownSearchKeydown);
	//Set the focus to our first field
	getElement('cts_CityTownName').focus();
	//Check if we have results to render
	if (data.result_count > 0) {
		reg.RenderCityTownSearchResults(data);
	}
}
reg.CityTownSearchUpdateKeyDown = function(dom_obj){
	if (dom_obj.key()['string']=='KEY_ENTER') {
		reg.CityTownSearchUpdate();
		dom_obj.stopPropagation();
	} else if (dom_obj.key()['string']=='KEY_ARROW_DOWN') {
		// Move the focus to the search area if there are search results
		reg.CityTownSearchKeydown(dom_obj);
	}
}
/*
	Perform a search (with updated inputs)
	The form must be rendered before this function will work.
*/
reg.CityTownSearchUpdate = function(){
	if (getNodeAttribute('CityTownSearchBox','class') == 'dialogbox') {
		var District = getElement('cts_District').value;
		var CityTownName = getElement('cts_CityTownName').value;
		var PostOffice = getElement('cts_PostOffice').value;
		var State = getElement('cts_State').value;
		var Block = getElement('cts_Block').value;
		var Country = getElement('cts_Country').value;
		
		var postVars = 'District='+District+'&CityTownName='+CityTownName+'&PostOffice='+PostOffice+'&State='+State+'&Block='+Block+'&Country='+Country;
		var d = postJSON('RegistrationCityTownSearch',postVars);
		d.addCallbacks(reg.RenderCityTownSearchResults,reg.error_report);
	}
}
/*
	Close the address city/town search box
*/
reg.CloseCityTownSearch = function() {
	swapDOM('CityTownSearchBox',null);
	swapDOM('CityTownSearchBoxShadow',null);
}
/*
	Handles the enter key for the search results
	and the up and down arrows to navigate the
	results
*/
reg.CityTownSearchKeydown = function(dom_obj){
	//get the current hi-lite row
	var rows = getElementsByTagAndClassName('LI','lite','CityTownSearchResults');
	if (rows.length == 0) {
		var rows = getElementsByTagAndClassName('LI',null,'CityTownSearchResults');
		if (rows.length == 0) {
			//exit the function if we have no results to work with
			return;
		}
		var row = rows[0];
		setNodeAttribute(row,'class','lite');
	} else {
		var row = rows[0];
	}
	//Process the even
	dom_obj.stop();
	if (dom_obj.key()['string']=='KEY_ENTER') {
		reg.SelectCityTownResult(dom_obj);
	} else if 	(dom_obj.key()['string']=='KEY_ARROW_UP') {
		//find the row before our selected row
		var rows = getElementsByTagAndClassName('LI',null,'CityTownSearchResults');
		if (rows.length > 1)  {
			//if the first row is selected, then we'll select the last row
			if (getNodeAttribute(rows[0],'class') == 'lite') {
				setNodeAttribute(rows[rows.length-1],'class','lite');
				setNodeAttribute(rows[0],'class',null);
			} else {
				for (i=0; i<rows.length; i++) {
					if (getNodeAttribute(rows[i+1],'class')=='lite') {
						setNodeAttribute(rows[i],'class','lite');
						setNodeAttribute(rows[i+1],'class',null);
						var buttons = getElementsByTagAndClassName('INPUT',null,rows[i]);
						buttons[0].focus();
						break;
					}
				}
			}
		} else if (rows.length == 1) {
			var buttons = getElementsByTagAndClassName('INPUT',null,rows[0]);
			buttons[0].focus();
		}
	} else if 	(dom_obj.key()['string']=='KEY_ARROW_DOWN') {
		//find the row after our selected row
		var rows = getElementsByTagAndClassName('LI',null,'CityTownSearchResults');
		//do nothing if the number of rows is 1
		if (rows.length > 1)  {
			//if the last row is selected, then we'll select the first row
			if (getNodeAttribute(rows[rows.length-1],'class') == 'lite') {
				setNodeAttribute(rows[rows.length-1],'class',null);
				setNodeAttribute(rows[0],'class','lite');
			} else {
				for (i=0; i<rows.length; i++) {
					if (getNodeAttribute(rows[i],'class')=='lite') {
						setNodeAttribute(rows[i+1],'class','lite');
						setNodeAttribute(rows[i],'class',null);
						var buttons = getElementsByTagAndClassName('INPUT',null,rows[i+1]);
						buttons[0].focus();
						break;
					}
				}
			}
		} else if (rows.length == 1) {
			var buttons = getElementsByTagAndClassName('INPUT',null,rows[0]);
			buttons[0].focus();
		}
	}
	dom_obj.stop();
}
/*
	After the search box is rendered, display any results that we have
*/
reg.RenderCityTownSearchResults = function(data){
	var AddResultRow = function(result){
		var row = createDOM('LI',null);
		var Button = createDOM('INPUT',{'style':'font-size:8px', 'type':'BUTTON','value':'Select', 'name':'btnSearchResultItem'});
		var ID = createDOM('INPUT',{'type':'HIDDEN','value':result.id,'name':'ID'});
		var Block = createDOM('INPUT',{'type':'HIDDEN','value':result.block,'name':'Block'});
		var District = createDOM('INPUT',{'type':'HIDDEN','value':result.district,'name':'District'});
		var CityTownName = createDOM('INPUT',{'type':'HIDDEN','value':result.city_town_name,'name':'CityTownName'});
		var PostOffice = createDOM('INPUT',{'type':'HIDDEN','value':result.post_office,'name':'PostOffice'});
		var State = createDOM('INPUT',{'type':'HIDDEN','value':result.state,'name':'State'});
		var Country = createDOM('INPUT',{'type':'HIDDEN','value':result.country,'name':'Country'});
		var Display = result.text;
		replaceChildNodes(row, Button,Display,ID,Block, District, CityTownName, PostOffice, State, Country);
		return row;
	}
	//Reset the message
	reg.toggle_message("");
	//Make our results list
	var SearchResults = getElement('CityTownSearchResults');
	replaceChildNodes(SearchResults,null);
	var results = data.results;
	for (i=0; i<results.length; i++) {
		var row = AddResultRow(results[i]);
		SearchResults.appendChild(row);
		//hi-lite the first row
		if (i==0) {
			setNodeAttribute(row,'class','lite');
		}
	}
	//Connect our buttons
	var Inputs = getElementsByTagAndClassName('INPUT',null,SearchResults);
	for (i=0; i<Inputs.length; i++) {
		if (getNodeAttribute(Inputs[i],'name')=='btnSearchResultItem') {
			connect(Inputs[i],'onclick',reg.SelectCityTownResult);
		}
	}
}
/*
	A click on the select button will call this function
	and store the result and values into the current form
*/
reg.SelectCityTownResult = function(dom_obj) {
	if (dom_obj.src().value == 'Select') {
		//In this case, someone pressed the "Select" button
		var row = dom_obj.src().parentNode;
	} else {
		var row = null;
		//In this case, someone pressed enter somewhere on the form.  Look for the item which is hi-lited
		var rows = getElementsByTagAndClassName('LI','lite','CityTownSearchResults');
		if (rows.length > 0) {
			row = rows[0];
		}
	}
	if (row != null) {
		var Inputs = getElementsByTagAndClassName('INPUT',null,row);
		for (i=0; i<Inputs.length; i++) {
			if (getNodeAttribute(Inputs[i],'name')=='Block') {
				getElement('Block').value = Inputs[i].value;
			} else if (getNodeAttribute(Inputs[i],'name')=='ID') {
				getElement('AddrCitytownNrID').value = Inputs[i].value;
			} else if (getNodeAttribute(Inputs[i],'name')=='District') {
				getElement('District').value = Inputs[i].value;
			} else if (getNodeAttribute(Inputs[i],'name')=='CityTownName') {
				getElement('CityTownName').value = Inputs[i].value;
			} else if (getNodeAttribute(Inputs[i],'name')=='PostOffice') {
				getElement('PostOffice').value = Inputs[i].value;
			} else if (getNodeAttribute(Inputs[i],'name')=='State') {
				getElement('State').value = Inputs[i].value;
			} else if (getNodeAttribute(Inputs[i],'name')=='Country') {
				getElement('Country').value = Inputs[i].value;
			}
		}
		var Text = scrapeText(row);
		replaceChildNodes('SelectedCity',Text);
	}
	reg.CloseCityTownSearch();
}
/*
	Ward OnChange: Render the new list of rooms for the ward
*/
reg.RenderRooms = function(data){
	var Option = function(id, name, selected) {
		if (selected) {
			var option = createDOM('OPTION',{'value':id,'selected':'selected'},name);
		} else {
			var option = createDOM('OPTION',{'value':id},name);
		}
		return option;
	}
	reg.toggle_message("");
	var Rooms = getElement('Room');
	var result = data.result;
	replaceChildNodes(Rooms,null);
	for (i=0;i<result.length;i++){
		if (i==0) {
			Rooms.appendChild(Option(result[i].id,result[i].name,true));
		} else {
			Rooms.appendChild(Option(result[i].id,result[i].name,false));
		}
	}
	reg.RoomOnChange(null);
}
/*
	Room OnChange: Render the new list of beds for the room
*/
reg.RenderBeds = function(data){
	var Option = function(value, selected) {
		if (selected) {
			var option = createDOM('OPTION',{'value':value,'selected':'selected'},value);
		} else {
			var option = createDOM('OPTION',{'value':value},value);
		}
		return option;
	}
	reg.toggle_message("");
	var Beds = getElement('Bed');
	var result = data.result;
	replaceChildNodes(Beds,null);
	for (i=0;i<result.length;i++){
		if (i==0) {
			Beds.appendChild(Option(result[i],true));
		} else {
			Beds.appendChild(Option(result[i],false));
		}
	}
}

//Configure our events using the Mochikit signal library
/* DEFINE OUR EVENT FUNCTIONS */
connect(document,'onkeydown', barcode.keydown);
connect(document,'onkeypress', barcode.keypress);
connect(document,'customerid', barcode.LoadCustomerID);
connect(document,'patientid', barcode.LoadPatientID);
//custom short-cuts
connect(document,'onkeypress',shortcuts.keypress);
connect(document,'onkeydown', shortcuts.keydown);
//Connect our buttons/fields to events -- need to do this on document load

connect(window, 'onload', function(){
		if (getElement("CityTownName")!=null) {
			connect("CityTownName",'onkeydown',reg.CityTownSearchKeyDown);
		}
		if (getElement("btnCityTown")!=null) {
			connect("btnCityTown",'onclick',reg.RenderCityTownSearch);
		}
		if (getElement("PostOffice")!=null) {
			connect("PostOffice",'onkeydown',reg.CityTownSearchKeyDown);
		}
		if (getElement("Block")!=null) {
			connect("Block",'onkeydown',reg.CityTownSearchKeyDown);
		}
		if (getElement("District")!=null) {
			connect("District",'onkeydown',reg.CityTownSearchKeyDown);
		}
		if (getElement("State")!=null) {
			connect("State",'onkeydown',reg.CityTownSearchKeyDown);
		}
		if (getElement("Country")!=null) {
			connect("Country",'onkeydown',reg.CityTownSearchKeyDown);
		}
		if (getElement("DateBirth")!=null) {
			connect("DateBirth",'onclick',reg.DatePick);
			connect("DateBirth",'onkeydown',reg.DatePick);
			connect("DateBirth",'onblur',reg.DatePickUpdate);
			reg.DateBirth = getElement("DateBirth").value;
		}
		if (getElement("Age")!=null) {
			connect("Age",'onblur',reg.AgePickUpdate);
			reg.Age = getElement("Age").value;
		}
		if (getElement("Ward")!=null) {
			connect("Ward",'onchange',reg.WardOnChange);
			connect("Room",'onchange',reg.RoomOnChange);
		}
		if (getElement("PatientType")!=null) {
			connect("PatientType",'onchange',reg.PatientTypeOnChange);
			reg.PatientTypeOnChange(null);
		}
	});
//Connect on onload for the document to open the document using javascript
connect(window, 'onload', reg.OpenOnLoad);


/*
	Small dialog box, for entering the customer id
*/
reg.customeriddialog_remove = function(){
	swapDOM('customerid_dialog',null);
	swapDOM('customerid_shadow',null);
}
reg.renderCustomerIdDialog = function(){
	var StringEdit = function(name, label, value){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',null);
		var edit = createDOM('INPUT',{'type':'text','name':name,'id':'dialog_'+name, 'value':value});
		data.appendChild(edit);
	  	row.appendChild(label);
	  	row.appendChild(data);
	  	return row;
	}
	reg.toggle_message("");
	//This is the big div box that surrounds the entire selection process
	var dialog = createDOM('DIV',{'class':'dialogbox','id':'customerid_dialog','style':'height:70px'});
	var shadow = createDOM('DIV',{'class':'dialogbox_shadow','id':'customerid_shadow','style':'height:80px'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:reg.customeriddialog_remove()'},"Close");
	dialog.appendChild(close_link);
	//The main table
	var table = createDOM('TABLE',{'class':'regular'});
	var tbody = createDOM('TBODY',null);
	// Add field
	tbody.appendChild(StringEdit('CustomerID','Customer ID',''));
	//Create our dialog
	table.appendChild(tbody);
	dialog.appendChild(table);
	document.body.appendChild(shadow);
	setOpacity(shadow,0.5);
	document.body.appendChild(dialog);
	//Attach the button event
	connect('dialog_CustomerID','onkeydown',shortcuts.keydown);
	getElement('dialog_CustomerID').focus();
}