/*
	My custom shortcuts:
	1. Open a dialog box for entering a an id
*/
var shortcuts = {};//keyboard short cut operations
shortcuts.keypress = function(e){
	if ((e.modifier()['ctrl'] == true) && (e.key()['string'] == 'l')) {
		e.stop();
		config.renderIdDialog();
	}
}
shortcuts.keydown = function(dom_obj){
	if (dom_obj.key()['string']=='KEY_ENTER') {
		var ID = getElement("dialog_ID");
		if ((ID != null) && (ID.value != null) && (ID.value != '')){
			//Load the items available for the customer
			config.idDialog_remove();
			var postVars = 'PersonellID='+ID.value;
			document.location.href = 'DoctorsEditor?'+postVars;
		}
	}
}

//AJAX Post function
function postJSON(url, postVars) {
	config.toggle_message("Sending request...");
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

var config = {};
config.FkDivID = null;
config.DateBirth = null;
config.Age = null;

config.collectPostVars = function(f){
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
      	postVars+= f.elements[i].name +'='+ encodeURIComponent(config.multiselect_csv(f.elements[i].id));
      } else {
      	postVars+= f.elements[i].name +'='+ encodeURIComponent(f.elements[i].options[f.elements[i].selectedIndex].value);
      }
    }
  }
  return postVars;
}

config.multiselect_csv = function(element_id){
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

config.clearAllFormFields = function(parentid){
	elems = getElementsByTagAndClassName('input',null,parentid);
	for (var i=0;i<elems.length;i++){
		elems[i].value = "";
	}
}

// AJSON reactions ==================
config.updated = function(data){
	var remove_message = function(data) {
		if (getNodeAttribute('last_result_msg','class') != null){
			swapDOM('last_result_msg',null);
		}
	}
	config.toggle_message("");
	if (data.message != null) {
		var display = createDOM('DIV',{'class':'displaymsg','id':'last_result_msg'},data.message);
		if (getNodeAttribute('last_result_msg','class') == null){
			document.body.appendChild(display);
		} else {
			swapDOM(field.id,display);
		}
	}
	var d = callLater(5,remove_message);
}
config.error_report = function(data){
	config.toggle_message("ERROR");
	var d = callLater(5,config.toggle_message);
}

config.toggle_message = function(message){
	var node_class = getNodeAttribute("json_status","class");
	if (node_class == null){
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		appendChildNodes(document.body,json_message);
	} else {
		var json_message = createDOM("DIV",{"id":"json_status", "class":"jsonmessage_on"},message);
		swapDOM("json_status",json_message);
	}
}

config.merge_hidden_inputs = function(parentid){
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
	Quick search
	Search for Items which match the entered text
*/
config.QuickSearch = function(dom_obj){
	if ((dom_obj.key()['string']=='KEY_ENTER')&&(getElement('QuickSearch').value!='')) {
		config.toggle_message("Searching...");
		var postVars = 'QuickSearchText='+getElement('QuickSearch').value;
		// The following line needs to point to the function which is used for the quick search in your context
		var d = postJSON('DoctorsEditorSearchDoctor',postVars);
		d.addCallbacks(config.RenderQuickSearch,config.error_report);
	}
}
/*
	If the Quick Search has the default text:
		Enter Search Text
	Then clear the text on clicking the box
*/
config.QuickSearchClear = function(dom_obj){
	if (getElement('QuickSearch').value == 'Enter Search Text'){
		getElement('QuickSearch').value = '';
	}
}
/* 	
	RenderQuickSearch: Render the Quick Search Results
*/
config.RenderQuickSearch = function(data){
	var AddResultRow = function(URL,PostVar,Text){
		var row = createDOM('LI',null);
		if (URL!=null) {
			var A = createDOM('A',{'href':URL+'?'+PostVar},Text);
		} else {
			var A = Text;
		}
		replaceChildNodes(row, A);
		return row;
	}
	//Reset the message
	config.toggle_message("");
	//Make our results list
	var QuickSearchResults = getElement('QuickSearchResults');
	replaceChildNodes(QuickSearchResults,null);
	var results = data.results;
	QuickSearchResults.appendChild(AddResultRow(null,null,'There are '+results.length+' result(s)'));
	for (i=0; i<results.length; i++) {
		QuickSearchResults.appendChild(AddResultRow('DoctorsEditor','PersonellID='+results[i].id,results[i].text));
	}
}/*
	Set the focus on the name field
*/
config.OpenOnLoad = function() {
	if (getElement('NameFirst')!=null) {
		getElement('NameFirst').focus();
	}
}
/*
	When someone enters an age, modify the DateBirth
	entry to match the age to the date.
*/
config.AgePickUpdate = function(dom_obj){
	var Age = getElement('Age').value;
	if (Age == '') {
		return false;
	} else if (isNaN(Age)){
		getElement('Age').value = '';
	} else if (Age != config.Age) {
		var Today = new Date();
		var DateBirth = new Date(Today.getFullYear() - Age, Today.getMonth(), Today.getDate());
		getElement('DateBirth').value = toISODate(DateBirth);
		config.Age = Age;
		config.DateBirth = toISODate(DateBirth);
	}
}
/*
	When a date has been entered, update
	the age box
*/
config.DatePickUpdate = function(dom_obj){
	var DateBirth = isoDate((getElement("DateBirth").value).slice(0,10));
	getElement('DateBirth').value = toISODate(DateBirth);
	if (getElement('DateBirth').value != config.DateBirth) {
		var Today = new Date();
		var diff = Today.getTime() - DateBirth.getTime();
		getElement('Age').value = parseInt((diff + 43200000)/(31557600000));
		config.Age = getElement('Age').value;
		config.DateBirth = toISODate(DateBirth);
	}
}
/*
	Call the search procedure and return the results below
*/
config.CityTownSearchKeyDown = function(dom_obj){
	if (dom_obj.key()['string']=='KEY_ENTER') {
		var Input = dom_obj.src();
		dom_obj.stop();
		config.toggle_message("Searching...");
		var postVars = Input.name + '=' + Input.value;
		var d = postJSON('DoctorsEditorCityTownSearch',postVars);
		d.addCallbacks(config.RenderCityTownSearch,config.error_report);
	}
}
/* 	Render the AddressCityTown search screen
	This is just the main part of the box, not the 
	search results
*/
config.RenderCityTownSearch = function(data){
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
	config.toggle_message("");
	//Remove any existing search box
	if (getNodeAttribute('CityTownSearchBox','class') == 'dialogbox') {
		config.CloseCityTownSearch();
	}
	var dialog = createDOM('DIV',{'style':'height:400px; width:400px', 'id':'CityTownSearchBox','class':'dialogbox'});
	var shadow = createDOM('DIV',{'id':'CityTownSearchBoxShadow','style':'height:410px;width:410px','class':'dialogbox_shadow'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:config.CloseCityTownSearch()'},"Close");
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
	connect('btnCityTownSearch','onclick',config.CityTownSearchUpdate);
	//Attach our Enter event
	var Inputs = getElementsByTagAndClassName('INPUT',null,table);
	for (i=0; i<Inputs.length; i++) {
		if (getNodeAttribute(Inputs[i],'type')=='text') {
			connect(Inputs[i],'onkeydown',config.CityTownSearchUpdateKeyDown);
		}
	}
	//connect the dialog box to another event handler for up/down arrow keys and enter key press outside the fields
	connect(dialog,'onkeydown',config.CityTownSearchKeydown);
	//Set the focus to our first field
	getElement('cts_CityTownName').focus();
	//Check if we have results to render
	if (data.result_count > 0) {
		config.RenderCityTownSearchResults(data);
	}
}
config.CityTownSearchUpdateKeyDown = function(dom_obj){
	if (dom_obj.key()['string']=='KEY_ENTER') {
		config.CityTownSearchUpdate();
		dom_obj.stopPropagation();
	} else if (dom_obj.key()['string']=='KEY_ARROW_DOWN') {
		// Move the focus to the search area if there are search results
		config.CityTownSearchKeydown(dom_obj);
	}
}
/*
	Perform a search (with updated inputs)
	The form must be rendered before this function will work.
*/
config.CityTownSearchUpdate = function(){
	if (getNodeAttribute('CityTownSearchBox','class') == 'dialogbox') {
		var District = getElement('cts_District').value;
		var CityTownName = getElement('cts_CityTownName').value;
		var PostOffice = getElement('cts_PostOffice').value;
		var State = getElement('cts_State').value;
		var Block = getElement('cts_Block').value;
		var Country = getElement('cts_Country').value;
		
		var postVars = 'District='+District+'&CityTownName='+CityTownName+'&PostOffice='+PostOffice+'&State='+State+'&Block='+Block+'&Country='+Country;
		var d = postJSON('DoctorsEditorCityTownSearch',postVars);
		d.addCallbacks(config.RenderCityTownSearchResults,config.error_report);
	}
}
/*
	Close the address city/town search box
*/
config.CloseCityTownSearch = function() {
	swapDOM('CityTownSearchBox',null);
	swapDOM('CityTownSearchBoxShadow',null);
}
/*
	Handles the enter key for the search results
	and the up and down arrows to navigate the
	results
*/
config.CityTownSearchKeydown = function(dom_obj){
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
		config.SelectCityTownResult(dom_obj);
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
config.RenderCityTownSearchResults = function(data){
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
	config.toggle_message("");
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
			connect(Inputs[i],'onclick',config.SelectCityTownResult);
		}
	}
}
/*
	A click on the select button will call this function
	and store the result and values into the current form
*/
config.SelectCityTownResult = function(dom_obj) {
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
	config.CloseCityTownSearch();
}
/*
	ForeignKey Select box
	
*/
config.FkSelect = function(e) {
	config.toggle_message("Loading...");
	if (e.src().id == 'btnPersonID') {
		config.FkDivID = 'PersonID'; // The DIV where we want to render our results later
		var d = postJSON('DoctorsEditorPersonSelect',null);
	}
	d.addCallbacks(config.RenderFkSelect,config.error_report);	
}
/*
	Render the ForeignKey selection dialog
*/
config.RenderFkSelect = function(data){
	var AddResultRow = function(value){
		//Each row needs: id, text, and selected
		var row = createDOM('DIV',{'class':'listingrow'},value.text);
		var btn = createDOM('INPUT',{'type':'button','value':'Select','name':'FkButton'});
		var text = createDOM('INPUT',{'type':'hidden','readonly':'readonly','value':value.text,'name':'FkText'});
		var id = createDOM('INPUT',{'type':'hidden','value':value.id,'name':'FkID'});
		//replaceChildNodes(Check, value.text);
		replaceChildNodes(row,btn,value.text,text,id);
		return row;
	}
	//Reset the message
	config.toggle_message("");
	//This is the big div box that surrounds the entire selection process
	var dialog = createDOM('DIV',{'class':'dialogbox','id':'fk_dialog','style':'height:200px; overflow:auto'});
	var shadow = createDOM('DIV',{'class':'dialogbox_shadow','id':'fk_shadow','style':'height:210px'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:config.FkSelect_remove()'},"Close");
	dialog.appendChild(close_link);
	document.body.appendChild(shadow);
	setOpacity(shadow,0.5);
	document.body.appendChild(dialog);
	//Create our SearchText box
	var SearchText = createDOM('INPUT',{'type':'text','name':'FkSearchText','id':'FkSearchText','value':''});
	dialog.appendChild(createDOM('BR',null));
	dialog.appendChild(SearchText);
	//Make our listing
	var SearchResults = createDOM('DIV',{'id':'FkResults'});
	dialog.appendChild(SearchResults);
	var results = data.results;
	for (i=0; i<results.length; i++) {
		SearchResults.appendChild(AddResultRow(results[i]));
	}
	//Attach the event to the buttons
	var Inputs = getElementsByTagAndClassName('INPUT',null,SearchResults);
	for (i=0;i<Inputs.length;i++){
		if (getNodeAttribute(Inputs[i],'type') == 'button') {
			connect(Inputs[i],'onclick',config.FkSelect_select);
		}
	}
	//Attach the update event to the search box
	connect(SearchText,'onkeydown',config.FkSelect_update);
	SearchText.focus();
	//We have a function name which we'll hide in the dialog box
	dialog.appendChild(createDOM('INPUT',{'type':'hidden','id':'FkFunction','value':data.function_name}));
}
//Remove the dialog box
config.FkSelect_remove = function(){
	swapDOM('fk_dialog',null);
	swapDOM('fk_shadow',null);
}
//Run a search to update the listing (usually to fine-tune the search results)
config.FkSelect_update = function(dom_obj){
	if ((dom_obj.key()['string']=='KEY_ENTER')&&(getElement('FkSearchText').value!='')) {
		config.toggle_message("Searching...");
		var postVars = 'SearchText='+getElement('FkSearchText').value;
		// The following line needs to point to the function which is used for the quick search in your context
		//alert(getElement('FkFunction').value);
		var d = postJSON(getElement('FkFunction').value,postVars);
		d.addCallbacks(config.RenderFkSelectUpdate,config.error_report);
	}
}
//Update the search results
config.RenderFkSelectUpdate = function(data){
	var AddResultRow = function(value){
		//Each row needs: id, text, and selected
		var row = createDOM('DIV',{'class':'listingrow'},value.text);
		var btn = createDOM('INPUT',{'type':'button','value':'Select','name':'FkButton'});
		var text = createDOM('INPUT',{'type':'hidden','readonly':'readonly','value':value.text,'name':'FkText'});
		var id = createDOM('INPUT',{'type':'hidden','value':value.id,'name':'FkID'});
		//replaceChildNodes(Check, value.text);
		replaceChildNodes(row,btn,value.text,text,id);
		return row;
	}
	//Reset the message
	config.toggle_message("");
	//Make our listing
	var SearchResults = getElement('FkResults');
	replaceChildNodes(SearchResults,null);
	var results = data.results;
	for (i=0; i<results.length; i++) {
		SearchResults.appendChild(AddResultRow(results[i]));
	}
	//Attach the event to the buttons
	var Inputs = getElementsByTagAndClassName('INPUT',null,SearchResults);
	for (i=0;i<Inputs.length;i++){
		if (getNodeAttribute(Inputs[i],'type') == 'button') {
			connect(Inputs[i],'onclick',config.FkSelect_select);
		}
	}
}
//Select and return an item from the list
config.FkSelect_select = function(dom_obj){
	var FkDiv = getElement(config.FkDivID);
	var elem = dom_obj.src().parentNode;
	var Inputs = getElementsByTagAndClassName('INPUT',null,elem);
	for (i=0; i<Inputs.length; i++){
		if (getNodeAttribute(Inputs[i],'name') == 'FkText') {
			var text = Inputs[i].value;
		} else if (getNodeAttribute(Inputs[i],'name') == 'FkID') {
			var ID = Inputs[i].value;
		}
	}
	replaceChildNodes(FkDiv,text,createDOM('INPUT',{'name':config.FkDivID,'type':'hidden','value':ID}));
	config.FkDivID = '';
	config.FkSelect_remove();
	//=========== Additional code not belonging to the normal foreign key operation
	// Un-Hide the DIV with information about saving a person as a doctor
	getElement('SaveInformation').style.display = 'table';
	// Hide the edit section
	getElement('part2').style.display = 'none';
	getElement('part3').style.display = 'none';
	getElement('part4').style.display = 'none';
	getElement('part5').style.display = 'none';
	//===========
}
/*
	Open a date entry javascript box
*/
config.DatePick = function(dom_obj){
	if ((dom_obj.type() == 'click') || (dom_obj.type()=='keydown' && (dom_obj.key()['string']=='KEY_ARROW_DOWN'))) {
		Widget.pickDateTime(dom_obj.src().id);
	}
}
//custom short-cuts
connect(document,'onkeypress',shortcuts.keypress);
connect(document,'onkeydown', shortcuts.keydown);
//Connect our buttons/fields to events -- need to do this on document load

connect(window, 'onload', function(){
	if (getElement("QuickSearch")!=null) {
		connect("QuickSearch",'onkeydown',config.QuickSearch);
		connect("QuickSearch",'onclick',config.QuickSearchClear);
	}
	if (getElement("btnPersonID")!=null) {
		connect("btnPersonID",'onclick',config.FkSelect);
	}
	//We have some inputs with the  dateEntry class which want to have a date control added
	var dateInputs = getElementsByTagAndClassName('INPUT',"dateEntry",document);
	for (i=0;i<dateInputs.length; i++){
		connect(dateInputs[i],"onclick",config.DatePick);
		connect(dateInputs[i],"onkeydown",config.DatePick);
	}
	if (getElement('btnDelete')!=null){
		connect('btnDelete','onclick',function(e) {
			if (!confirm('Are you sure you want to delete?')) {
				e.stop();
			}
		});
	}
	if (getElement("CityTownName")!=null) {
		connect("CityTownName",'onkeydown',config.CityTownSearchKeyDown);
	}
	if (getElement("btnCityTown")!=null) {
		connect("btnCityTown",'onclick',config.RenderCityTownSearch);
	}
	if (getElement("PostOffice")!=null) {
		connect("PostOffice",'onkeydown',config.CityTownSearchKeyDown);
	}
	if (getElement("Block")!=null) {
		connect("Block",'onkeydown',config.CityTownSearchKeyDown);
	}
	if (getElement("District")!=null) {
		connect("District",'onkeydown',config.CityTownSearchKeyDown);
	}
	if (getElement("State")!=null) {
		connect("State",'onkeydown',config.CityTownSearchKeyDown);
	}
	if (getElement("Country")!=null) {
		connect("Country",'onkeydown',config.CityTownSearchKeyDown);
	}
	if (getElement("Age")!=null) {
		connect("Age",'onblur',config.AgePickUpdate);
		config.Age = getElement("Age").value;
	}
	if (getElement("DateBirth")!=null) {
		connect("DateBirth",'onblur',config.DatePickUpdate);
		config.DateBirth = getElement("DateBirth").value;
	}
});
//Connect on onload for the document to open the document using javascript
connect(window, 'onload', config.OpenOnLoad);

/*
	Small dialog box, to enter an id for direct loading
*/
config.idDialog_remove = function(){
	swapDOM('id_dialog',null);
	swapDOM('id_shadow',null);
}
config.renderIdDialog = function(){
	var StringEdit = function(name, label, value){
		var row = createDOM('TR',null);
		var label = createDOM('TD',label);
		var data = createDOM('TD',null);
		var edit = createDOM('INPUT',{'type':'text','name':name,'id':'dialog_ID', 'value':value});
		data.appendChild(edit);
	  	row.appendChild(label);
	  	row.appendChild(data);
	  	return row;
	}
	config.toggle_message("");
	//This is the big div box that surrounds the entire selection process
	var dialog = createDOM('DIV',{'class':'dialogbox','id':'id_dialog','style':'height:70px'});
	var shadow = createDOM('DIV',{'class':'dialogbox_shadow','id':'id_shadow','style':'height:80px'});
	//Close link
	var close_link = createDOM('A',{'href':'javascript:config.idDialog_remove()'},"Close");
	dialog.appendChild(close_link);
	//The main table
	var table = createDOM('TABLE',{'class':'regular'});
	var tbody = createDOM('TBODY',null);
	// Add field *********************************************** Edit this name
	tbody.appendChild(StringEdit('PersonellID','Personell ID',''));
	//Create our dialog
	table.appendChild(tbody);
	dialog.appendChild(table);
	document.body.appendChild(shadow);
	setOpacity(shadow,0.5);
	document.body.appendChild(dialog);
	//Attach the button event
	getElement('dialog_ID').focus();
}
