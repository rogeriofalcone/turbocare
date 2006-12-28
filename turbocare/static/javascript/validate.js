/*
	Validate
	
	Javascript for validating form inputs in a standard way
	Generic Date vaidation.   All my date fields will have basic validation if they are of the "dateEntry" class
*/
validate = {};

/*
	DateValidate: Make sure that the date is either:
		blank or greater than or equal to 1970-01-01
		and in ISO format
*/
validate.DateValidate = function(dom_obj) {
	var input = dom_obj.src();
	if (isNaN(input.value[0])) {// a relative date using text
		/*	Options for relative dates include
			Last Day or Last # Days (e.g. "Last 3 Days" or "Last 22 Days")
			Last Week or Last # Weeks (e.g. "Last 3 Weeks" or "Last 22 Weeks")
			Last Month or Last # Months
			Last Year or Last # Years
			Next Day or Next # Days (e.g. "Next 3 Days" or "Next 22 Days")
			Next Week or Next # Weeks
			Next Month or Next # Months
			Next Year or Next # Years
			NOTE: For now, the code approximates time, i.e. 1 Year = 365 days, 1 month = 30 days, 1 week = 7 days.
		*/
		var strArr = input.value.split(' ');
		var valid = '';
		if (strArr.length == 1) {
			if ((strArr[0].toLowerCase()=='l') || (strArr[0].toLowerCase()=='last')) {
				var valid = "Last 1 Days";
			} else if ((strArr[0].toLowerCase()=='n') || (strArr[0].toLowerCase()=='next')){
				var valid = "Next 1 Days";
			}
		} else if (strArr.length == 2) {
			if ((strArr[0].toLowerCase()=='l') || (strArr[0].toLowerCase()=='last')) {
				if (isNaN(strArr[1])) {
					var str2 = strArr[1].toLowerCase();
					if (str2 == 'd' || str2 == 'day' || str2 == 'days') {
						var valid = "Last 1 Days";
					} else if (str2 == 'w' || str2 == 'week' || str2 == 'weeks') {
						var valid = "Last 1 Weeks";
					} else if (str2 == 'm' || str2 == 'month' || str2 == 'months') {
						var valid = "Last 1 Months";
					} else if (str2 == 'y' || str2 == 'year' || str2 == 'years') {
						var valid = "Last 1 Years";
					}
				} else {
					var valid = "Last " + strArr[1] + " Days";
				}
			} else if ((strArr[0].toLowerCase()=='n') || (strArr[0].toLowerCase()=='next')){
				if (isNaN(strArr[1])) {
					var str2 = strArr[1].toLowerCase();
					if (str2 == 'd' || str2 == 'day' || str2 == 'days') {
						var valid = "Next 1 Days";
					} else if (str2 == 'w' || str2 == 'week' || str2 == 'weeks') {
						var valid = "Next 1 Weeks";
					} else if (str2 == 'm' || str2 == 'month' || str2 == 'months') {
						var valid = "Next 1 Months";
					} else if (str2 == 'y' || str2 == 'year' || str2 == 'years') {
						var valid = "Next 1 Years";
					}
				} else {
					var valid = "Next " + strArr[1] + " Days";
				}
			}
		} else if (strArr.length >= 3) {
			if ((strArr[0].toLowerCase()=='l') || (strArr[0].toLowerCase()=='last')) {
				if (isNaN(strArr[1])) {
					var str2 = strArr[1].toLowerCase();
					if (str2 == 'd' || str2 == 'day' || str2 == 'days') {
						var valid = "Last 1 Days";
					} else if (str2 == 'w' || str2 == 'week' || str2 == 'weeks') {
						var valid = "Last 1 Weeks";
					} else if (str2 == 'm' || str2 == 'month' || str2 == 'months') {
						var valid = "Last 1 Months";
					} else if (str2 == 'y' || str2 == 'year' || str2 == 'years') {
						var valid = "Last 1 Years";
					}
				} else {
					var str3 = strArr[2].toLowerCase();
					if (str3 == 'd' || str3 == 'day' || str3 == 'days') {
						var valid = "Last " + strArr[1] + " Days";
					} else if (str3 == 'w' || str3 == 'week' || str3 == 'weeks') {
						var valid = "Last " + strArr[1] + " Weeks";
					} else if (str3 == 'm' || str3 == 'month' || str3 == 'months') {
						var valid = "Last " + strArr[1] + " Months";
					} else if (str3 == 'y' || str3 == 'year' || str3 == 'years') {
						var valid = "Last " + strArr[1] + " Years";
					}
				}
			} else if ((strArr[0].toLowerCase()=='n') || (strArr[0].toLowerCase()=='next')){
				if (isNaN(strArr[1])) {
					var str2 = strArr[1].toLowerCase();
					if (str2 == 'd' || str2 == 'day' || str2 == 'days') {
						var valid = "Next 1 Days";
					} else if (str2 == 'w' || str2 == 'week' || str2 == 'weeks') {
						var valid = "Next 1 Weeks";
					} else if (str2 == 'm' || str2 == 'month' || str2 == 'months') {
						var valid = "Next 1 Months";
					} else if (str2 == 'y' || str2 == 'year' || str2 == 'years') {
						var valid = "Next 1 Years";
					}
				} else {
					var str3 = strArr[2].toLowerCase();
					if (str3 == 'd' || str3 == 'day' || str3 == 'days') {
						var valid = "Next " + strArr[1] + " Days";
					} else if (str3 == 'w' || str3 == 'week' || str3 == 'weeks') {
						var valid = "Next " + strArr[1] + " Weeks";
					} else if (str3 == 'm' || str3 == 'month' || str3 == 'months') {
						var valid = "Next " + strArr[1] + " Months";
					} else if (str3 == 'y' || str3 == 'year' || str3 == 'years') {
						var valid = "Next " + strArr[1] + " Years";
					}
				}
			}
		}
		input.value = valid;
	// Date formatted date expected
	} else {// It's a date formatted number
		try {
			var d = isoTimestamp(input.value);
			if (d=='Invalid Date' || d==null) {
				throw new Error('Bad Date Format');
			}
			input.value = toISOTimestamp(d);
		} catch (e) {
			try {
				//Grab the first part, only the date portion for parsing
				var part1 = input.value.split(' ')[0];
				var d = new Date(Date.parse(part1));
				if (d=='Invalid Date') {
					throw new Error('Bad Date Format');
				}
				input.value = toISODate(d);
			} catch (ee) {
				input.value = '';
			}
		}
	}
}

connect(window, 'onload', function(){
		//We have some inputs with the  dateEntry class which want to have a date control added
		var dateInputs = getElementsByTagAndClassName('INPUT',"dateEntry",document);
		for (i=0;i<dateInputs.length; i++){
			connect(dateInputs[i],"onblur",validate.DateValidate);
		}
});